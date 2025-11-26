import Sidebar from './Sidebar';
import React from 'react';

const Layout = ({ children }) => {
    return (
        <div className="flex h-screen bg-gray-100 overflow-hidden">
            {/* Sidebar fijo a la izquierda */}
            <Sidebar />

            {/* Área de contenido principal (scrolleable) */}
            <main className="flex-1 overflow-y-auto p-8">
                <div className="max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;