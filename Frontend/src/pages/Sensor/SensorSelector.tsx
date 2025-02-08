import type { Sensor, NodeType } from './Sensor_data';
// import { Button } from '@/components/ui/button';
import { Leaf, Droplets, Activity, Sun, Wind } from 'lucide-react';
import { motion } from 'framer-motion';

interface SensorSelectorProps {
  sensors: Sensor[];
  selectedSensors: Sensor[];
  toggleSensor: (sensor: Sensor) => void;
  activeNode: NodeType;
}

const sensorIcons = {
  temp: Leaf,
  humid: Droplets,
  motion: Activity,
  light: Sun,
  air: Wind,
};

export default function SensorSelector({
  sensors,
  selectedSensors,
  toggleSensor,
  activeNode,
}: SensorSelectorProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {sensors.map((sensor) => {
        const isSelected = selectedSensors.some(
          (s) => s.id === sensor.id && s.nodeType === activeNode,
        );
        const Icon = sensorIcons[sensor.id as keyof typeof sensorIcons];
        return (
          <motion.div
            key={sensor.id}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <div
              className={`h-full flex flex-col p-6 border rounded-lg shadow transition-all duration-300 ease-in-out ${
                isSelected
                  ? 'border-emerald-500 shadow-lg shadow-emerald-200'
                  : 'border-teal-200'
              }`}
            >
              <div className="pb-2 flex-grow">
                <h3 className="flex items-center text-xl font-bold text-emerald-700">
                  <Icon className="mr-2 h-6 w-6" />
                  {sensor.name}
                </h3>
                <p className="text-emerald-500 text-sm">
                  {sensor.description}
                </p>
              </div>
              <div>
                <p className="text-2xl font-bold text-emerald-800 mb-3">
                  ${sensor.price}
                </p>
                <button
                  className={`w-full py-2 rounded text-white font-bold transition-colors ${
                    isSelected
                      ? 'bg-emerald-600 hover:bg-emerald-700'
                      : 'bg-teal-600 hover:bg-teal-700'
                  }`}
                  onClick={() => toggleSensor(sensor)}
                >
                  {isSelected ? 'Remove' : 'Add to ' + activeNode}
                </button>
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
