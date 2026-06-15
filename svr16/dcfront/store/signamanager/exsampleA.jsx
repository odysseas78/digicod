"use client";
import React, { useEffect, useState } from 'react';
import { signalManagerRegistry } from './lastsm';

function ComponentA() {
    const storageKey = 'appState';
    const manager = signalManagerRegistry.getManager(storageKey);

    // Initialisieren der Eigenschaften, falls noch nicht vorhanden
    if (!manager.proxy.key1) manager.add('key1', 456);
    if (!manager.proxy.key2) manager.add('key2', 75);
    if (!manager.proxy.key3) manager.add('key3', { key31: 89, key32: 77 });

    // Nutzung von proxy für reaktiven Zugriff
    const [key1, setKey1] = useState(manager.proxy.key1.value);
    const [key2, setKey2] = useState(manager.proxy.key2.value);
    const [key31, setKey31] = useState(manager.proxy.key3.key31);

    useEffect(() => {
        // Abonnieren der Signale zur Aktualisierung des States
        const unsubscribe1 = manager.proxy.key1.subscribe(setKey1);
        const unsubscribe2 = manager.proxy.key2.subscribe(setKey2);
        const unsubscribe31 = manager.proxy.key3.key31.subscribe(setKey31);

        // Aufräumen der Abonnements beim Unmounten
        return () => {
            unsubscribe1();
            unsubscribe2();
            unsubscribe31();
        };
    }, [manager]);

    const handleIncrement = () => {
        manager.proxy.key1.value += 1; // Änderung über proxy
    };

    return (
        <div>
            <h2>Component A</h2>
            <p>key1: {key1}</p>
            <p>key2: {key2}</p>
            <p>key3.key31: {key31}</p>
            <button onClick={handleIncrement}>Increment key1</button>
        </div>
    );
}

export default ComponentA;
