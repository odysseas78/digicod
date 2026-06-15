"use client";
import { signal, Signal } from '@preact/signals-react';

export class SignalManager {
    constructor(storageKey) {
        this.storageKey = storageKey;
        // this.save = save;
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
        // if (this.save !== 'save') return {}
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
        // if (this.save !== 'save') return {}
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






class SignalManagerRegistry {
    constructor() {
        this.managers = {}; // storageKey -> SignalManager Instanz
    }

    /**
     * Gibt die SignalManager-Instanz für den gegebenen storageKey zurück.
     * Erstellt eine neue Instanz, wenn sie noch nicht existiert.
     *
     * @param {string} storageKey - Der Schlüssel für localStorage und zur Identifizierung der Instanz.
     * @returns {SignalManager} - Die SignalManager-Instanz.
     */
    getManager(storageKey) {
        console.log(`SignalManagerRegistry: getManager aufgerufen mit storageKey = "${storageKey}"`);
        console.trace(); // Gibt die aktuelle Stapelverfolgung aus

        if (!this.managers[storageKey]) {
            this.managers[storageKey] = new SignalManager(storageKey);
            console.log(`SignalManagerRegistry: Neue SignalManager-Instanz für "${storageKey}" erstellt.`);
        } else {
            console.log(`SignalManagerRegistry: Bestehende SignalManager-Instanz für "${storageKey}" verwendet.`);
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
            console.log(`SignalManagerRegistry: SignalManager-Instanz für "${storageKey}" entfernt.`);
        }
    }


}


// Exportieren einer Singleton-Instanz der Registry
export const signalManagerRegistry = new SignalManagerRegistry();

const w = []
export function getOrCreateStore(target) {
    return new Proxy(target, {
      set(obj, prop, value) {
        self.manager = signalManagerRegistry.getManager(obj.store)
        if(manager.proxy[prop === undefined]) {
          manager.addProperty(prop, value)
        } else {
          manager.proxy[prop] = value
        }
        return manager.proxy; // Indiziert, dass das Set erfolgreich war
      },
      get(obj, prop) {
        return self.manager.proxy[prop]; // Indiziert, dass das Set erfolgreich war
      }
    });
  }
// const storageKey = 'appState';
// const manager = signalManagerRegistry.getManager(storageKey);
// manager.addProperty('key1', 456);
// const h = manager.proxy
// console.log(h.key1.value);

// h.key1.value += 1;
// console.log(h.key1.value);

// const o = {
//     manager(key, value){
//         return `manager.addProperty(${key},${value})`
//     },
    
//     $gt:0,
//     get gt(){
//         return this.$gt
//     },

//     set gt(d){
//         return this.$gt = signalManagerRegistry.getManager(d)
//     }
// }

// o.gt = 'Store_1'
// console.log(o);
// console.log(o.gt);

// const w = []
// function createSignalProxy(target) {
//     return new Object(target, {
//       set(obj, prop, value) {
//         // console.log(obj);
//         // console.log();
//         // console.log(value);
//         // w.push(obj)
//         // w.push(prop)
//         // w.push(value)
//         // Bedingung: Hier können Sie Ihre spezifischen Bedingungen prüfen
//         // Beispiel: Alle neuen Werte werden in Signale umgewandelt

       
//         return true; // Indiziert, dass das Set erfolgreich war
//       },
//       get(obj, prop) {
//         return obj[prop];
//       }
//     });
//   }

  
//   Verwendung des Proxies
// const p = createSignalProxy();



// p.kk = 65
// console.log(p);






// const storageKey = 'appState';
// const manager = signalManagerRegistry.getManager(storageKey);
// manager.addProperty('key1', 456);
// const h = manager.proxy
// console.log(h.key1.value);

// h.key1.value += 1;
// console.log(h.key1.value);

// const dd = {

//     $gt:0,

//     get gt(){
//         return this.$gt
//     },

//     set gt(d){
//         signalManagerRegistry.getManager(storageKey);
//         return this.$gt += d
//     }
// }
// dd.hzgtfrd = 'Store_58'

// dd.gt = 5

// const g = dd.gt = 7

// console.log(g);



// function Jstr(obj){
//     const f = JSON.stringify(obj)
//     console.log(f);
//     const g = JSON.parse(f)
//     console.log(g);
// }




// Jstr(gg)

const obj = {
    "storageKey": "GetCategory",
    "save": "save",
    "subscribedSignals": {},
    "saveTimeout": null,
    "state": {
      "0": {
        "id": 28,
        "name": "Mobile Recharge",
        "pf_name": "Mobile",
        "slug": "mobile",
        "active": true
      },
      "1": {
        "id": 27,
        "name": "Payment Cards",
        "pf_name": "PaymentCard",
        "slug": "paymentcards",
        "active": true
      },
      "2": {
        "id": 26,
        "name": "Gift Cards",
        "pf_name": "GiftCard",
        "slug": "giftcards",
        "active": true
      },
      "3": {
        "id": 1,
        "name": "Region Free",
        "pf_name": "region free",
        "slug": "region-free",
        "active": true
      },
      "error": "Request failed with status code 503",
      "origin": [
        {
          "id": 28,
          "name": "Mobile Recharge",
          "pf_name": "Mobile",
          "slug": "mobile",
          "active": true
        },
        {
          "id": 27,
          "name": "Payment Cards",
          "pf_name": "PaymentCard",
          "slug": "paymentcards",
          "active": true
        },
        {
          "id": 26,
          "name": "Gift Cards",
          "pf_name": "GiftCard",
          "slug": "giftcards",
          "active": true
        },
        {
          "id": 1,
          "name": "Region Free",
          "pf_name": "region free",
          "slug": "region-free",
          "active": true
        }
      ],
      "selected": "giftcards"
    }}

// const sm = new SignalManager('Store_1').createProxy({})

// sm.sasasa = 789

// console.log(sm.sasasa);

// sm.kk = 789

// console.log(sm.kk);

// sm.uu = obj

// console.log(sm.uu);
// console.log(sm);






