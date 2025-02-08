import { useState } from 'react';
import type { Sensor, NodeType, Feature } from './Sensor_data';
import { motion, AnimatePresence } from 'framer-motion';

interface FeaturesListProps {
  sensors: Sensor[];
  selectedSensors: Sensor[];
  activeNode: NodeType;
}

export default function FeaturesList({
  sensors,
  selectedSensors,
  activeNode,
}: FeaturesListProps) {
  const [expandedFeature, setExpandedFeature] = useState<string | null>(null);

  const toggleFeature = (featureId: string) => {
    setExpandedFeature(expandedFeature === featureId ? null : featureId);
  };

  const getFeatureStatus = (
    feature: Feature,
    sensorId: string,
  ): 'unlocked' | 'locked' => {
    return selectedSensors.some(
      (s) => s.id === sensorId && s.nodeType === activeNode,
    )
      ? 'unlocked'
      : 'locked';
  };

  return (
    <div className="overflow-hidden bg-white shadow-xl border rounded-lg">
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white p-4">
        <h2 className="text-2xl font-bold">
          {activeNode === 'base' ? 'Base Node Features' : 'Child Node Features'}
        </h2>
      </div>
      <div className="p-0">
        <ul className="divide-y divide-emerald-100">
          {sensors.flatMap((sensor) =>
            sensor.features.map((feature) => (
              <li key={feature.id} className="overflow-hidden">
                <button
                  onClick={() => toggleFeature(feature.id)}
                  className="w-full text-left px-4 py-3 flex items-center justify-between hover:bg-emerald-50 transition-colors duration-150"
                >
                  <span className="font-medium text-emerald-800">
                    {feature.name}
                  </span>
                  <div className="flex items-center">
                    <span
                      className={`mr-2 text-sm font-semibold ${
                        getFeatureStatus(feature, sensor.id) === 'unlocked'
                          ? 'text-emerald-600'
                          : 'text-gray-500'
                      }`}
                    >
                      {getFeatureStatus(feature, sensor.id) === 'unlocked'
                        ? 'Unlocked'
                        : 'Locked'}
                    </span>
                    {expandedFeature === feature.id ? '🔼' : '🔽'}
                  </div>
                </button>
                <AnimatePresence>
                  {expandedFeature === feature.id && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="bg-emerald-50 px-4 py-3"
                    >
                      <p className="text-sm text-emerald-700 mb-2">
                        {feature.description}
                      </p>
                      <div className="flex items-center">
                        <span className="text-xs font-medium text-emerald-600 mr-2">
                          Provided by:
                        </span>
                        <span className="text-xs font-bold text-emerald-800">
                          {sensor.name}
                        </span>
                      </div>
                      <div
                        className={`mt-2 flex items-center text-sm ${
                          getFeatureStatus(feature, sensor.id) === 'unlocked'
                            ? 'text-emerald-600'
                            : 'text-gray-500'
                        }`}
                      >
                        {getFeatureStatus(feature, sensor.id) === 'unlocked'
                          ? '✔ Available for this node'
                          : `🔒 Add ${sensor.name} to unlock`}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </li>
            )),
          )}
        </ul>
      </div>
    </div>
  );
}