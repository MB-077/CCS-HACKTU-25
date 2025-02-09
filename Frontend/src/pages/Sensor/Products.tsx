import { useState } from 'react';
import type { Sensor } from './Sensor_data';
import { motion } from 'framer-motion';

interface ProductsProps {
  selectedSensors: Sensor[];
  totalPrice: number;
}

export default function Products({
  selectedSensors,
  totalPrice,
}: ProductsProps) {
  const baseNodeSensors = selectedSensors?.filter((s) => s?.nodeType === 'base');
  const childNodeSensors = selectedSensors?.filter((s) => s.nodeType === 'child');

  return (
    <div className="bg-white shadow-xl overflow-hidden border rounded-lg">
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white p-4">
        <h2 className="text-2xl font-bold">Your Ecosystem Summary</h2>
      </div>
      <div className="p-6">
        {selectedSensors?.length > 0 ? (
          <>
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-emerald-800 mb-2">
                Base Node Sensors
              </h3>
              <ul className="space-y-1">
                {baseNodeSensors.map((sensor) => (
                  <motion.li
                    key={sensor.id}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="flex justify-between text-emerald-700 bg-emerald-50 px-3 py-2 rounded-md"
                  >
                    <span>{sensor.name}</span>
                    <span>₹{sensor.price}</span>
                  </motion.li>
                ))}
              </ul>
            </div>
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-emerald-800 mb-2">
                Child Node Sensors
              </h3>
              <ul className="space-y-1">
                {childNodeSensors.map((sensor) => (
                  <motion.li
                    key={sensor.id}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="flex justify-between text-emerald-700 bg-teal-50 px-3 py-2 rounded-md"
                  >
                    <span>{sensor.name}</span>
                    <span>₹{sensor.price}</span>
                  </motion.li>
                ))}
              </ul>
            </div>
            <div className="text-2xl font-bold text-emerald-800 flex justify-between items-center mt-4 pt-4 border-t border-emerald-200">
              <span>Total:</span>
              <span>₹{totalPrice}</span>
            </div>
          </>
        ) : (
          <p className="text-emerald-600">Select sensors to build your ecosystem.</p>
        )}
      </div>
      <div className="p-4">
        <button
          className="w-full py-2 rounded text-white font-bold transition-colors bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
          disabled={selectedSensors?.length === 0}
        >
          {selectedSensors?.length > 0 ? 'Purchase Ecosystem' : 'Select Sensors'}
        </button>
      </div>
    </div>
  );
}