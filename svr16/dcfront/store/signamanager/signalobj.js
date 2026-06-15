"use client";
import { signal, Signal } from '@preact/signals-react';

export class SignalManager {
    /**
     * Konstruktor für SignalManager.
     * @param {string} storageKey - Schlüssel für localStorage.
     * @param {boolean} save - Ob der Zustand gespeichert werden soll.
     * @param {Array<string>} excludedKeys - Liste von Pfaden, die nicht in Signale umgewandelt werden sollen.
     * @param {object} initialState - Initialer Zustand.
     */
    constructor(storageKey, save = true, excludedKeys = [], initialState = {}) {
        this.storageKey = storageKey;
        this.save = save;
        this.excludedKeys = excludedKeys;
        this.subscribedSignals = new Set(); // Set zur Verfolgung abonnierter Signale
        this.saveTimeout = null; // Timeout-ID für Debouncing

        // Laden des Zustands aus localStorage, falls save=true, sonst initialState
        const loadedState = this.loadState();

        // Merge initialState into loadedState
        this.state = this.mergeStates(loadedState, initialState);

        // Erstellen des Proxys mit dem kombinierten Zustand
        this.proxy = this.createProxy(this.state, '');
        this.subscribeAll(this.proxy, '');
    }

    /**
     * Prüft, ob ein gegebener Pfad in den ausgeschlossenen Schlüsseln ist.
     * @param {string} path - Der aktuelle Pfad.
     * @returns {boolean} - Ob der Pfad ausgeschlossen ist.
     */
    isExcluded(path) {
        return this.excludedKeys.some(excludedPath => {
            return path === excludedPath || path.startsWith(`${excludedPath}.`);
        });
    }

    /**
     * Lädt den gespeicherten Zustand aus localStorage und deserialisiert ihn.
     */
    loadState() {
        if (!this.save) return {};
        try {
            const savedState = JSON.parse(localStorage.getItem(this.storageKey));
            if (savedState) {
                return this.deserialize(savedState, '');
            }
        } catch (error) {
            console.error('Fehler beim Laden des Zustands:', error);
        }
        return {};
    }

    /**
     * Speichert den gesamten Zustand in localStorage mit Debouncing.
     */
    saveState() {
        if (!this.save) return;
        try {
            if (this.saveTimeout) clearTimeout(this.saveTimeout);
            this.saveTimeout = setTimeout(() => {
                const plainObject = this.serialize(this.proxy);
                localStorage.setItem(this.storageKey, JSON.stringify(plainObject));
                this.saveTimeout = null;
            }, 300); // 300ms Verzögerung (Debouncing)
        } catch (error) {
            console.error('Fehler beim Speichern des Zustands:', error);
        }
    }

    /**
     * Deserialisiert das gespeicherte Objekt in Signale und verschachtelte Proxys.
     * @param {object} obj - Das zu deserialisierende Objekt.
     * @param {string} currentPath - Der aktuelle Pfad.
     * @returns {object} - Das deserialisierte Objekt mit Signalen und Proxys.
     */
    deserialize(obj, currentPath) {
        const result = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                const value = obj[key];
                const newPath = currentPath ? `${currentPath}.${key}` : key;
                if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                    // Rekursiv verschachtelte Objekte behandeln, falls nicht ausgeschlossen
                    if (this.isExcluded(newPath)) {
                        result[key] = value; // Keine Umwandlung
                    } else {
                        result[key] = this.createProxy(this.deserialize(value, newPath), newPath);
                    }
                } else {
                    if (this.isExcluded(newPath)) {
                        result[key] = value; // Keine Umwandlung
                    } else {
                        result[key] = signal(value);
                    }
                }
            }
        }
        return result;
    }

    /**
     * Serialisiert das Proxy-Objekt rekursiv in ein einfaches Objekt.
     * @param {object} obj - Das zu serialisierende Proxy-Objekt.
     * @returns {object} - Das serialisierte Objekt.
     */
    serialize(obj) {
        const plainObject = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                const value = obj[key];
                if (value instanceof Signal) {
                    plainObject[key] = value.value;
                } else if (typeof value === 'object' && value !== null) {
                    plainObject[key] = this.serialize(value); // Rekursive Serialisierung
                } else {
                    plainObject[key] = value;
                }
            }
        }
        return plainObject;
    }

    /**
     * Erstellt einen Proxy für das gegebene Objekt, um Änderungen zu überwachen.
     * @param {object} target - Das Zielobjekt.
     * @param {string} currentPath - Der aktuelle Pfad.
     * @returns {Proxy} - Der erstellte Proxy.
     */
    createProxy(target, currentPath) {
        const self = this;
        const handler = {
            set(obj, prop, value) {
                const newPath = currentPath ? `${currentPath}.${prop}` : prop;
                if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                    // Rekursiv verschachtelte Objekte in Proxys umwandeln, falls nicht ausgeschlossen
                    if (self.isExcluded(newPath)) {
                        obj[prop] = value; // Keine Umwandlung
                    } else {
                        obj[prop] = self.createProxy(self.deserialize(value, newPath), newPath);
                    }
                } else {
                    if (self.isExcluded(newPath)) {
                        obj[prop] = value; // Keine Umwandlung
                    } else {
                        if (!(value instanceof Signal)) {
                            obj[prop] = signal(value);
                        } else {
                            obj[prop] = value;
                        }
                    }
                }
                self.subscribeSignal(obj[prop]);
                self.saveState();
                return true;
            },
            get(obj, prop) {
                
                return obj[prop];
            }
        };
        return new Proxy(target, handler);
    }

    /**
     * Rekursiv alle Signale im Objekt abonnieren.
     * @param {object} obj - Das zu abonnierende Objekt.
     * @param {string} currentPath - Der aktuelle Pfad.
     */
    subscribeAll(obj, currentPath) {
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                const value = obj[key];
                const newPath = currentPath ? `${currentPath}.${key}` : key;
                if (value instanceof Signal) {
                    this.subscribeSignal(value);
                } else if (typeof value === 'object' && value !== null) {
                    this.subscribeAll(value, newPath); // Rekursiv abonnieren
                }
            }
        }
    }

    /**
     * Abonniert ein einzelnes Signal, falls es noch nicht abonniert ist.
     * @param {Signal} signalInstance - Die Signal-Instanz.
     */
    subscribeSignal(signalInstance) {
        if (this.subscribedSignals.has(signalInstance)) {
            // Bereits abonniert
            return;
        }
        if (signalInstance instanceof Signal) {
            signalInstance.subscribe(() => {
                this.saveState();
            });
            this.subscribedSignals.add(signalInstance); // Markieren als abonniert
        }
    }

    /**
     * Fügt eine neue Eigenschaft zum Zustand hinzu.
     * @param {string} key - Der Schlüssel der neuen Eigenschaft.
     * @param {*} initialValue - Der Anfangswert der neuen Eigenschaft.
     */
    addProperty(key, initialValue) {
        this.proxy[key] = initialValue;
    }

    /**
     * Setzt eine Eigenschaft zurück, ohne das Speichern zu triggern.
     * @param {string} key - Der Schlüssel der Eigenschaft.
     * @param {*} value - Der neue Wert der Eigenschaft.
     */
    resetProperty(key, value) {
        if (this.proxy[key] instanceof Signal) {
            this.proxy[key].value = value;
        } else {
            this.proxy[key] = value;
        }
        this.saveState();
    }

    /**
     * Importiert ein JSON-Objekt in den Zustand.
     * @param {object} jsonObject - Das zu importierende JSON-Objekt.
     */
    fromJSON(jsonObject) {
        for (const key in jsonObject) {
            if (jsonObject.hasOwnProperty(key)) {
                this.proxy[key] = jsonObject[key]; // Setzen über den Proxy
            }
        }
        this.saveState(); // Optional: Speichern nach dem Import
    }

    /**
     * Hilfsfunktion zum Zusammenführen von zwei Zuständen.
     * @param {object} target - Das Zielobjekt.
     * @param {object} source - Das Quellobjekt.
     * @returns {object} - Das zusammengeführte Objekt.
     */
    mergeStates(target, source) {
        for (const key in source) {
            if (source.hasOwnProperty(key)) {
                const sourceValue = source[key];
                if (typeof sourceValue === 'object' && sourceValue !== null && !Array.isArray(sourceValue)) {
                    if (!target[key] || typeof target[key] !== 'object') {
                        target[key] = {};
                    }
                    this.mergeStates(target[key], sourceValue);
                } else {
                    target[key] = sourceValue;
                }
            }
        }
        return target;
    }
}


class SignalManagerRegistry {
    constructor() {
        this.managers = {}; // storageKey -> SignalManager Instanz
    }

    /**
     * Gibt die SignalManager-Instanz für den gegebenen storageKey zurück.
     * Erstellt eine neue Instanz, wenn sie noch nicht existiert.
     *
     * @param {string} storageKey - Der Schlüssel für localStorage und zur Identifizierung der Instanz.
     * @param {object} options - Optionen für den SignalManager (save, excludedKeys, initialState).
     * @returns {SignalManager} - Die SignalManager-Instanz.
     */
    getManager(storageKey, options = {}) {
        // console.log(`SignalManagerRegistry: getManager aufgerufen mit storageKey = "${storageKey}"`);
       // console.trace(); // Gibt die aktuelle Stapelverfolgung aus

        if (!this.managers[storageKey]) {
            this.managers[storageKey] = new SignalManager(
                storageKey,
                options.save !== undefined ? options.save : true,
                options.excludedKeys || [],
                options.initialState || {}
            );
            // console.log(`SignalManagerRegistry: Neue SignalManager-Instanz für "${storageKey}" erstellt.`);
        } else {
            // console.log(`SignalManagerRegistry: Bestehende SignalManager-Instanz für "${storageKey}" verwendet.`);
        }
        return this.managers[storageKey];
    }

    /**
     * Entfernt eine SignalManager-Instanz aus der Registry.
     *
     * @param {string} storageKey - Der Schlüssel der zu entfernenden Instanz.
     */
    removeManager(storageKey) {
        if (this.managers[storageKey]) {
            delete this.managers[storageKey];
            // console.log(`SignalManagerRegistry: SignalManager-Instanz für "${storageKey}" entfernt.`);
        }
    }
}

// Exportieren einer Singleton-Instanz der Registry
export const signalManagerReg = new SignalManagerRegistry();
