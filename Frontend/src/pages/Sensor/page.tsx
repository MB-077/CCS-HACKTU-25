'use client';

import { useState } from 'react';
import { sensors, type Sensor, type NodeType } from './Sensor_data';
import  SensorSelector  from './SensorSelector';
import  FeaturesList  from './feature_list';
import Products from './Products';

export default function PricingPage() {
  const [selectedSensors, setSelectedSensors] = useState<Sensor[]>([]);
  const [activeNode, setActiveNode] = useState<NodeType>('base');

  const toggleSensor = (sensor: Sensor) => {
    setSelectedSensors((prev) => {
      const isAlreadySelected = prev.some(
        (s) => s.id === sensor.id && s.nodeType === activeNode,
      );
      if (isAlreadySelected) {
        return prev.filter(
          (s) => !(s.id === sensor.id && s.nodeType === activeNode),
        );
      }
      if (prev.filter((s) => s.nodeType === activeNode).length >= 10) {
        alert(`You can't add more than 10 sensors to a ${activeNode} node.`);
        return prev;
      }
      return [...prev, { ...sensor, nodeType: activeNode }];
    });
  };

  const totalPrice = selectedSensors.reduce(
    (sum, sensor) => sum + sensor.price,
    0,
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-emerald-100 py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-5xl font-bold text-center text-emerald-800 mb-4">
          Build Your IoT Ecosystem
        </h1>
        <p className="text-xl text-center text-emerald-600 mb-12">
          Select sensors for your base and child nodes to unlock powerful
          features
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            <div className="flex justify-center space-x-4 mb-6">
              <button
                onClick={() => setActiveNode('base')}
                className={`px-6 py-2 rounded-full text-lg font-semibold transition-colors ${
                  activeNode === 'base'
                    ? 'bg-emerald-600 text-white'
                    : 'bg-white text-emerald-600 hover:bg-emerald-100'
                }`}
              >
                Base Node
              </button>
              <button
                onClick={() => setActiveNode('child')}
                className={`px-6 py-2 rounded-full text-lg font-semibold transition-colors ${
                  activeNode === 'child'
                    ? 'bg-emerald-600 text-white'
                    : 'bg-white text-emerald-600 hover:bg-emerald-100'
                }`}
              >
                Child Node
              </button>
            </div>
            <SensorSelector
              sensors={sensors}
              selectedSensors={selectedSensors}
              toggleSensor={toggleSensor}
              activeNode={activeNode}
            />
          </div>
          <div className="space-y-8">
            <FeaturesList
              sensors={sensors}
              selectedSensors={selectedSensors}
              activeNode={activeNode}
            />
            <Products
              selectedSensors={selectedSensors}
              totalPrice={totalPrice}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
