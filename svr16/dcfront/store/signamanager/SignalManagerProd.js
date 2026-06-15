"use client";
import { signal, Signal } from '@preact/signals-react';

/**
 * Manager für rekursiven Zustand (Preact Signals) mit optionalem localStorage-Persist.
 */
class SignalManager {
    constructor(storageKey, save = true, excludedKeys = [], initialState = {}) {
        this.storageKey = storageKey;
        this.save = save;
        this.excludedKeys = excludedKeys;
        this.subscribedSignals = new Set();
        this.saveTimeout = null;

        // Zustand laden (sofern gewünscht) und mit initialState mergen
        const loadedState = this.loadState();
        this.state = this.mergeStates(loadedState, initialState);

        // Proxy erstellen
        this.proxy = this.createProxy(this.state, '');
        // Alle vorhandenen Signale abonnieren
        this.subscribeAll(this.proxy, '');
    }

    // ----------------------------
    //      EXCLUDE-LOGIK
    // ----------------------------
    isExcluded(path) {
        return this.excludedKeys.some(excludedPath => {
            return path === excludedPath || path.startsWith(`${excludedPath}.`);
        });
    }

    // ----------------------------
    //      STORAGE
    // ----------------------------
    loadState() {
        if (!this.save) return {};
        try {
            const savedState = localStorage.getItem(this.storageKey);
            if (savedState) {
                const parsed = JSON.parse(savedState);
                return this.deserialize(parsed, '');
            }
        } catch (error) {
            console.error('Fehler beim Laden des Zustands:', error);
        }
        return {};
    }

    saveState() {
        if (!this.save) return;
        try {
            if (this.saveTimeout) {
                clearTimeout(this.saveTimeout);
            }
            this.saveTimeout = setTimeout(() => {
                const plainObj = this.serialize(this.proxy, '');
                localStorage.setItem(this.storageKey, JSON.stringify(plainObj));
                this.saveTimeout = null;
            }, 300);
        } catch (error) {
            console.error('Fehler beim Speichern des Zustands:', error);
        }
    }

    // ----------------------------
    //      SERIALISIERUNG
    // ----------------------------
    /**
     * Deserialisieren: Rekursiv in Signale umwandeln (sofern nicht ausgeschlossen).
     * @param {any} obj
     * @param {string} currentPath
     * @param {WeakSet} visited - zur Erkennung zirkulärer Referenzen
     */
    deserialize(obj, currentPath, visited = new WeakSet()) {
        if (typeof obj !== 'object' || obj === null) {
            return obj;
        }
        if (visited.has(obj)) {
            // Zirkulärer Verweis erkannt -> optional ignorieren oder Warnung
            return obj;
        }
        visited.add(obj);

        // Array oder Objekt?
        const result = Array.isArray(obj) ? [] : {};
        const keys = Object.keys(obj);

        for (const key of keys) {
            const value = obj[key];
            const newPath = currentPath ? `${currentPath}.${key}` : key;

            if (this.isExcluded(newPath)) {
                // Nichts konvertieren
                result[key] = value;
            } else if (typeof value === 'object' && value !== null) {
                // Rekursive Deserialisierung
                // Anschließend Proxy => so werden innere Änderungen abgefangen
                const nested = this.deserialize(value, newPath, visited);
                result[key] = this.createProxy(nested, newPath);
            } else {
                // Normaler Wert => Signal
                result[key] = signal(value);
            }
        }

        return result;
    }

    /**
     * Serialisieren: Rekursiv Proxy/Signale in plain JS-Objekt umwandeln.
     * @param {any} obj
     * @param {string} currentPath
     * @param {WeakSet} visited - zur Erkennung zirkulärer Referenzen
     */
    serialize(obj, currentPath, visited = new WeakSet()) {
        if (typeof obj !== 'object' || obj === null) {
            return obj;
        }
        if (visited.has(obj)) {
            // Zirkulärer Verweis -> breche ab oder gib etwas anderes zurück
            return null;
        }
        visited.add(obj);

        const isArr = Array.isArray(obj);
        const plain = isArr ? [] : {};

        const keys = Object.keys(obj); 
        for (const key of keys) {
            const value = obj[key];
            const newPath = currentPath ? `${currentPath}.${key}` : key;

            // if excluded -> aussparen oder unberührt übernehmen
            if (this.isExcluded(newPath)) {
                // Variante 1: komplett überspringen
                // continue;

                // Variante 2: unverändert speichern
                plain[key] = value instanceof Signal ? value.value : value;
                continue;
            }

            if (value instanceof Signal) {
                plain[key] = value.value;
            } else if (typeof value === 'object' && value !== null) {
                plain[key] = this.serialize(value, newPath, visited);
            } else {
                plain[key] = value;
            }
        }

        return plain;
    }

    // ----------------------------
    //      PROXY
    // ----------------------------
    createProxy(target, currentPath) {
        const self = this;
        return new Proxy(target, {
            set(obj, prop, value) {
                const newPath = currentPath ? `${currentPath}.${prop}` : prop;

                if (typeof value === 'object' && value !== null) {
                    if (self.isExcluded(newPath)) {
                        obj[prop] = value; // unverändert
                    } else {
                        // Zuerst deserialisieren -> innere Strukturen proxifizieren
                        const deserialized = self.deserialize(value, newPath);
                        obj[prop] = self.createProxy(deserialized, newPath);
                    }
                } else {
                    if (self.isExcluded(newPath)) {
                        obj[prop] = value;
                    } else {
                        // Normaler Wert in Signal umwandeln
                        obj[prop] = value instanceof Signal ? value : signal(value);
                    }
                }

                // Abo einrichten
                self.subscribeSignal(obj[prop]);
                // Speichern
                self.saveState();
                return true;
            },
            get(obj, prop) {
                return obj[prop];
            }
        });
    }

    // ----------------------------
    //      SIGNAL-ABO
    // ----------------------------
    subscribeAll(obj, currentPath) {
        if (typeof obj !== 'object' || obj === null) return;

        const keys = Object.keys(obj);
        for (const key of keys) {
            const value = obj[key];
            const newPath = currentPath ? `${currentPath}.${key}` : key;

            if (value instanceof Signal) {
                this.subscribeSignal(value);
            } else if (typeof value === 'object' && value !== null) {
                this.subscribeAll(value, newPath);
            }
        }
    }

    subscribeSignal(signalInstance) {
        if (!(signalInstance instanceof Signal)) return;
        if (!this.subscribedSignals.has(signalInstance)) {
            signalInstance.subscribe(() => {
                this.saveState();
            });
            this.subscribedSignals.add(signalInstance);
        }
    }

    // ----------------------------
    //      ÖFFENTLICHE METHODEN
    // ----------------------------
    addProperty(key, initialValue) {
        this.proxy[key] = initialValue;
    }

    resetProperty(key, value) {
        if (this.proxy[key] instanceof Signal) {
            this.proxy[key].value = value;
        } else {
            this.proxy[key] = value;
        }
        this.saveState();
    }

    removeProperty(key) {
        if (key in this.proxy) {
            delete this.proxy[key];
            this.saveState();
        }
    }

    fromJSON(jsonObject) {
        for (const key of Object.keys(jsonObject)) {
            this.proxy[key] = jsonObject[key];
        }
        this.saveState();
    }

    clearLocalStorage() {
        if (this.save && this.storageKey) {
            localStorage.removeItem(this.storageKey);
        }
    }

    mergeStates(target, source) {
        for (const key of Object.keys(source)) {
            const sourceValue = source[key];
            if (
                typeof sourceValue === 'object' &&
                sourceValue !== null &&
                !Array.isArray(sourceValue)
            ) {
                if (!target[key] || typeof target[key] !== 'object') {
                    target[key] = {};
                }
                this.mergeStates(target[key], sourceValue);
            } else {
                target[key] = sourceValue;
            }
        }
        return target;
    }
}

// -----------------------------------------
//   Registry (Singleton)
// -----------------------------------------
class SignalManagerRegistry {
    constructor() {
        this.managers = {};
    }

    getManager(storageKey, options = {}) {
        if (!this.managers[storageKey]) {
            this.managers[storageKey] = new SignalManager(
                storageKey,
                options.save ?? true,
                options.excludedKeys ?? [],
                options.initialState ?? {}
            );
        }
        return this.managers[storageKey];
    }

    removeManager(storageKey) {
        if (this.managers[storageKey]) {
            delete this.managers[storageKey];
        }
    }
}

export const signalManagerRegFull = new SignalManagerRegistry();

