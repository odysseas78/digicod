"use client";
import React, { useEffect, useState } from 'react';
import { signalManagerRegistry } from './lastsm';

function ComponentB() {
    const storageKey = 'appState';
    const manager = signalManagerRegistry.getManager(storageKey);

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

    const handleUpdate = () => {
        manager.proxy.key2.value = 'Updated Value'; // Änderung über proxy
        manager.proxy.key3.key31.value += 100; // Änderung an verschachtelter Eigenschaft über proxy
    };

    return (
        <div>
            <h2>Component B</h2>
            <p>key1: {key1}</p>
            <p>key2: {key2}</p>
            <p>key3.key31: {key31}</p>
            <button className={'p-5 bg-slate-500'} onClick={handleUpdate}>Update key2 and key3.key31</button>
        </div>
    );
}

export default ComponentB;
