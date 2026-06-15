"use client";
import { signal, Signal } from '@preact/signals-react';

export class SignalManager2 {
    constructor(storageKey, save) {
        this.storageKey = storageKey;
        this.save = save;
        this.subscribedKeys = new Set();
        this.saveTimeout = null; // Timeout-ID für Debouncing
        this.state = this.loadState();
        this.proxy = this.createProxy(this.state);
        this.subscribeAll();
    }


    // Laden des gespeicherten Zustands aus localStorage
    loadState() {
        if (this.save !== 'save') return {}
        try {
            const savedState = JSON.parse(localStorage.getItem(this.storageKey));
            if (savedState) {
                const state = {};
                for (const key in savedState) {
                    state[key] = signal(savedState[key]);
                }
                return state;
            }
        } catch (error) {
            console.error('Fehler beim Laden des Zustands:', error);
        }
        return {};
    }

    saveState() {
        if (this.save !== 'save') return {}
        try {
            if (this.saveTimeout) clearTimeout(this.saveTimeout);
            this.saveTimeout = setTimeout(() => {
                const plainObject = {};
                for (const key in this.proxy) {
                    if (this.proxy[key] instanceof Signal) {
                        plainObject[key] = this.proxy[key].value;
                    } else {
                        plainObject[key] = this.proxy[key];
                    }
                }
                localStorage.setItem(this.storageKey, JSON.stringify(plainObject));
                this.saveTimeout = null;
            }, 300);
        } catch (error) {
            console.error('Fehler beim Speichern des Zustands:', error);
        }
    }


    // Erstellen eines Proxys, um das Hinzufügen neuer Eigenschaften zu überwachen
    createProxy(target) {
        const handler = {
            set: (obj, prop, value) => {
                if (!(value instanceof Signal)) {
                    obj[prop] = signal(value);
                    this.subscribeSignal(prop, obj[prop]);
                } else {
                    obj[prop] = value;
                    this.subscribeSignal(prop, value);
                }
                this.saveState();
                return true;
            },
            get: (obj, prop) => {
                return obj[prop];
            }
        };
        return new Proxy(target, handler);
    }

    // Abonnieren aller bestehenden Signale
    subscribeAll() {
        for (const key in this.proxy) {
            if (this.proxy[key] instanceof Signal) {
                this.subscribeSignal(key, this.proxy[key]);
            }
        }
    }

    // Abonnieren eines einzelnen Signals nur einmal
    subscribeSignal(key, signalInstance) {
        if (this.subscribedKeys.has(key)) {
            // Bereits abonniert, nichts tun
            return;
        }
        signalInstance.subscribe(() => {
            this.saveState();
        });
        this.subscribedKeys.add(key); // Markiere als abonniert
    }

    // Methode zum Hinzufügen neuer Eigenschaften
    add(key, initialValue) {
        this.proxy[key] = initialValue;
    }

    // Methode zum Zurücksetzen einer Eigenschaft ohne Speicherung (optional)
    resetProperty(key, value) {
        if (this.proxy[key] instanceof Signal) {
            this.proxy[key].value = value;
        } else {
            this.proxy[key] = value;
        }
        this.saveState();
    }

    // Methode zum Importieren eines JSON-Objekts
    fromJSON(jsonObject) {
        const processObject = (obj) => {
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
                        // Wenn der Wert ein verschachteltes Objekt ist, rekursiv verarbeiten
                        processObject(obj[key]);
                    }
                    this.proxy[key] = obj[key];
                }
            }
        };

        processObject(jsonObject);
        this.saveState(); // Optional: Speichern nach dem Import
    }

}




// SignalManager.js

class SignalManager3 {
    constructor(storageKey, save = null) {
        this.storageKey = storageKey;
        this.save = save;
        this.subscribedKeys = new Set(); // Set zur Verfolgung abonnierter Signale
        this.saveTimeout = null; // Timeout-ID für Debouncing
        this.state = this.loadState();
        this.proxy = this.createProxy(this.state);
        this.subscribeAll();
    }

    // Laden des gespeicherten Zustands aus localStorage
    loadState() {
        if (this.save !== 'save') return {}
        try {
            const savedState = JSON.parse(localStorage.getItem(this.storageKey));
            if (savedState) {
                return savedState;
            }
        } catch (error) {
            console.error('Fehler beim Laden des Zustands:', error);
        }
        return {};
    }

    // Speichern des gesamten Zustands in localStorage mit Debouncing
    saveState() {
        if (this.save !== 'save') return {}
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
     * Serialisiert das Proxy-Objekt rekursiv, um den Zustand zu speichern.
     *
     * @param {object} obj - Das Proxy-Objekt.
     * @returns {object} - Das serialisierte Objekt.
     */
    serialize(obj) {
        const plainObject = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                if (obj[key] instanceof Signal) {
                    plainObject[key] = obj[key].value;
                } else if (typeof obj[key] === 'object' && obj[key] !== null) {
                    plainObject[key] = this.serialize(obj[key]);
                } else {
                    plainObject[key] = obj[key];
                }
            }
        }
        return plainObject;
    }

    /**
     * Erstellt einen Proxy für das gegebene Objekt und behandelt verschachtelte Objekte rekursiv.
     *
     * @param {object} target - Das Zielobjekt.
     * @returns {Proxy} - Der erstellte Proxy.
     */
    createProxy(target) {
        const self = this;
        const handler = {
            set(obj, prop, value) {
                if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                    // Wenn der Wert ein verschachteltes Objekt ist, erstelle einen verschachtelten Proxy
                    obj[prop] = self.createProxy(value);
                } else {
                    if (!(value instanceof Signal)) {
                        obj[prop] = signal(value);
                    } else {
                        obj[prop] = value;
                    }
                }
                self.subscribeSignal(prop, obj[prop]);
                self.saveState();
                return true;
            },
            get(obj, prop) {
                return obj[prop];
            }
        };
        return new Proxy(target, handler);
    }

    // Abonnieren aller bestehenden Signale
    subscribeAll(obj = this.proxy) {
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                const value = obj[key];
                if (value instanceof Signal) {
                    this.subscribeSignal(key, value);
                } else if (typeof value === 'object' && value !== null) {
                    this.subscribeAll(value); // Rekursive Abonnement für verschachtelte Objekte
                }
            }
        }
    }

    // Abonnieren eines einzelnen Signals nur einmal
    subscribeSignal(key, signalInstance) {
        if (this.subscribedKeys.has(key)) {
            // Bereits abonniert, nichts tun
            return;
        }
        if (signalInstance instanceof Signal) {
            signalInstance.subscribe(() => {
                this.saveState();
            });
            this.subscribedKeys.add(key); // Markiere als abonniert
        }
    }

    // Methode zum Hinzufügen neuer Eigenschaften
    add(key, initialValue) {
        this.proxy[key] = initialValue;
    }

    // Methode zum Zurücksetzen einer Eigenschaft ohne Speicherung (optional)
    resetProperty(key, value) {
        if (this.proxy[key] instanceof Signal) {
            this.proxy[key].value = value;
        } else {
            this.proxy[key] = value;
        }
        this.saveState();
    }

    // Methode zum Importieren eines JSON-Objekts
    fromJSON(jsonObject) {
        for (const key in jsonObject) {
            if (jsonObject.hasOwnProperty(key)) {
                const value = jsonObject[key];
                if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                    this.proxy[key] = this.createProxy(value);
                } else {
                    this.proxy[key] = value instanceof Signal ? value : signal(value);
                }
            }
        }
        this.saveState(); // Optional: Speichern nach dem Import
    }
}

export class SignalManager4 {
    constructor(storageKey, save) {
        this.storageKey = storageKey;
        this.save = save;
        this.subscribedKeys = new Set(); // Set zur Verfolgung abonnierter Signale
        this.saveTimeout = null; // Timeout-ID für Debouncing
        this.state = this.loadState();
        this.proxy = this.createProxy(this.state);
        this.subscribeAll();
    }

    // Laden des gespeicherten Zustands aus localStorage
    loadState() {
        if (this.save !== 'save') return {}
        try {
            const savedState = JSON.parse(localStorage.getItem(this.storageKey));
            if (savedState) {
                return savedState;
            }
        } catch (error) {
            console.error('Fehler beim Laden des Zustands:', error);
        }
        return {};
    }

    // Speichern des gesamten Zustands in localStorage mit Debouncing
    saveState() {
        if (this.save !== 'save') return {}
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
     * Serialisiert das Proxy-Objekt rekursiv, um den Zustand zu speichern.
     *
     * @param {object} obj - Das Proxy-Objekt.
     * @returns {object} - Das serialisierte Objekt.
     */
    serialize(obj) {
        const plainObject = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                if (obj[key] instanceof Signal) {
                    plainObject[key] = obj[key].value;
                } else if (typeof obj[key] === 'object' && obj[key] !== null) {
                    plainObject[key] = this.serialize(obj[key]);
                } else {
                    plainObject[key] = obj[key];
                }
            }
        }
        return plainObject;
    }

    /**
     * Erstellt einen Proxy für das gegebene Objekt und behandelt verschachtelte Objekte rekursiv.
     *
     * @param {object} target - Das Zielobjekt.
     * @returns {Proxy} - Der erstellte Proxy.
     */
    createProxy(target) {
        const self = this;
        const handler = {
            set(obj, prop, value) {
                if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                    // Wenn der Wert ein verschachteltes Objekt ist, erstelle einen verschachtelten Proxy
                    obj[prop] = self.createProxy(value);
                } else {
                    if (!(value instanceof Signal)) {
                        obj[prop] = signal(value);
                    } else {
                        obj[prop] = value;
                    }
                }
                self.subscribeSignal(prop, obj[prop]);
                self.saveState();
                return true;
            },
            get(obj, prop) {
                return obj[prop];
            }
        };
        return new Proxy(target, handler);
    }

    // Abonnieren aller bestehenden Signale
    subscribeAll(obj = this.proxy) {
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                const value = obj[key];
                if (value instanceof Signal) {
                    this.subscribeSignal(key, value);
                } else if (typeof value === 'object' && value !== null) {
                    this.subscribeAll(value); // Rekursive Abonnement für verschachtelte Objekte
                }
            }
        }
    }

    // Abonnieren eines einzelnen Signals nur einmal
    subscribeSignal(key, signalInstance) {
        if (this.subscribedKeys.has(key)) {
            // Bereits abonniert, nichts tun
            return;
        }
        if (signalInstance instanceof Signal) {
            signalInstance.subscribe(() => {
                this.saveState();
            });
            this.subscribedKeys.add(key); // Markiere als abonniert
        }
    }

    // Methode zum Hinzufügen neuer Eigenschaften
    add(key, initialValue) {
        this.proxy[key] = initialValue;
    }

    // Methode zum Zurücksetzen einer Eigenschaft ohne Speicherung (optional)
    resetProperty(key, value) {
        if (this.proxy[key] instanceof Signal) {
            this.proxy[key].value = value;
        } else {
            this.proxy[key] = value;
        }
        this.saveState();
    }

    // Methode zum Importieren eines JSON-Objekts
    fromJSON(jsonObject) {
        for (const key in jsonObject) {
            if (jsonObject.hasOwnProperty(key)) {
                const value = jsonObject[key];
                if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                    this.proxy[key] = this.createProxy(value);
                } else {
                    this.proxy[key] = value instanceof Signal ? value : signal(value);
                }
            }
        }
        this.saveState(); // Optional: Speichern nach dem Import
    }
}


// SignalManager.js


export class SignalManager {
    constructor(storageKey, save) {
        this.storageKey = storageKey;
        this.save = save;
        this.subscribedSignals = new Set(); // Set zur Verfolgung abonnierter Signale
        this.saveTimeout = null; // Timeout-ID für Debouncing
        this.state = this.loadState();
        this.proxy = this.createProxy(this.state);
        this.subscribeAll(this.proxy);
    }

    /**
     * Lädt den gespeicherten Zustand aus localStorage und deserialisiert ihn.
     */
    loadState() {
        if (this.save !== 'save') return {}
        try {
            const savedState = JSON.parse(localStorage.getItem(this.storageKey));
            if (savedState) {
                return this.deserialize(savedState);
            }
        } catch (error) {
            console.error('Fehler beim Laden des Zustands:', error);
        }
        return {};
    }

    /**
     * Deserialisiert das gespeicherte Objekt in Signale und verschachtelte Proxys.
     * @param {object} obj - Das zu deserialisierende Objekt.
     * @returns {object} - Das deserialisierte Objekt mit Signalen und Proxys.
     */
    deserialize(obj) {
        const result = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                const value = obj[key];
                if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                    // Rekursiv verschachtelte Objekte behandeln
                    result[key] = this.createProxy(this.deserialize(value));
                } else {
                    // Primitive Werte in Signale umwandeln
                    result[key] = signal(value);
                }
            }
        }
        return result;
    }

    /**
     * Speichert den gesamten Zustand in localStorage mit Debouncing.
     */
    saveState() {
        if (this.save !== 'save') return {}
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
     * @returns {Proxy} - Der erstellte Proxy.
     */
    createProxy(target) {
        const self = this;
        const handler = {
            set(obj, prop, value) {
                if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                    // Rekursiv verschachtelte Objekte in Proxys umwandeln
                    obj[prop] = self.createProxy(self.deserialize(value));
                } else {
                    if (!(value instanceof Signal)) {
                        obj[prop] = signal(value);
                    } else {
                        obj[prop] = value;
                    }
                }
                self.subscribeSignal(prop, obj[prop]);
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
     */
    subscribeAll(obj) {
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                const value = obj[key];
                if (value instanceof Signal) {
                    this.subscribeSignal(key, value);
                } else if (typeof value === 'object' && value !== null) {
                    this.subscribeAll(value); // Rekursiv abonnieren
                }
            }
        }
    }

    /**
     * Abonniert ein einzelnes Signal, falls es noch nicht abonniert ist.
     * @param {string} key - Der Schlüssel des Signals.
     * @param {Signal} signalInstance - Die Signal-Instanz.
     */
    subscribeSignal(key, signalInstance) {
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
    add(key, initialValue) {
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
        this.proxy['origin'] = jsonObject
        for (const key in jsonObject) {
            if (jsonObject.hasOwnProperty(key)) {
                this.proxy[key] = jsonObject[key]; // Setzen über den Proxy
                // this.proxy[key+'origin']
            }
        }
        this.saveState(); // Optional: Speichern nach dem Import
    }
}

// ###########################################################################

class SignalManagerRegistry {
    constructor() {
        // Ein Objekt zur Speicherung von SignalManager-Instanzen anhand ihres storageKey
        this.managers = {};
    }

    /**
     * Gibt die SignalManager-Instanz für den gegebenen storageKey zurück.
     * Erstellt eine neue Instanz, wenn sie noch nicht existiert.
     *
     * @param {string} storageKey - Der Schlüssel für localStorage und zur Identifizierung der Instanz.
     * @returns {SignalManager} - Die SignalManager-Instanz.
     */
    getManager(storageKey, save) {
        if (!this.managers[storageKey]) {
            this.managers[storageKey] = new SignalManager(storageKey, save);
        }
        return this.managers[storageKey];
    }

    /**
     * Optionale Methode zum Entfernen einer SignalManager-Instanz.
     *
     * @param {string} storageKey - Der Schlüssel der zu entfernenden Instanz.
     */
    removeManager(storageKey) {
        if (this.managers[storageKey]) {
            delete this.managers[storageKey];
        }
    }
}

// Exportieren einer Singleton-Instanz der Registry
export const signalManagerRegistry = new SignalManagerRegistry();

