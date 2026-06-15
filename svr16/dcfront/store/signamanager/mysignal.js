"use client";
import { signal, Signal } from '@preact/signals-react';

export class SignalManager {
    constructor(storageKey) {
        this.storageKey = storageKey;
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
}

export  function smp(store_id){
    return new SignalManager(store_id).proxy
  }

export  function sm(store_id){
    return new SignalManager(store_id)
  }
