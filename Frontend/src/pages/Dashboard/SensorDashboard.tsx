import React, { useState, useEffect } from 'react';
import { Tab } from '@headlessui/react';
import CardDataStats from '../../components/CardDataStats';
import ChartOne from '../../components/Charts/ChartOne';
import Pusher from 'pusher-js'; // Updated import

interface BaseNodeData {
  atmosphericPressure?: number;
  solarIntensity?: number;
  humidity?: number;
  temperature?: number;
  soilMoisture?: number;
  ambientLight?: { r: number; g: number; b: number };
  gasSensors?: { mq2: number; mq135: number };
  relayState?: string;
  waterFlowRate?: number;
}

interface ChildNodeData {
  humidity?: number;
  soilMoisture?: number;
  soilTemperature?: number;
  rainDropIntensity?: number;
}

const SensorDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'base' | 'child'>('base');
  const [baseNodeData, setBaseNodeData] = useState<BaseNodeData>({});
  const [childNodeData, setChildNodeData] = useState<ChildNodeData>({});

  useEffect(() => {
    const pusher = new Pusher(process.env.REACT_APP_PUSHER_KEY as string, {
      cluster: process.env.REACT_APP_PUSHER_CLUSTER,
    });

    const channel = pusher.subscribe("sensor-AGRI_001");
    channel.bind("sensor-update", (data) => {
      setBaseNodeData({
        atmosphericPressure: data.atm_pressure,
        solarIntensity: data.lux,
        humidity: data.dht11_humidity,
        temperature: data.dht11_temperature,
        soilMoisture: data.soil_moisture_percent_1,
        ambientLight: { r: data.apds_red, g: data.apds_green, b: data.apds_blue },
        gasSensors: { mq2: data.mq_2_percent, mq135: data.mq_135_percent },
        relayState: data.relayState || 'off',
        waterFlowRate: data.flow,
      });

      setChildNodeData({
        humidity: data.node_dht11_humidity,
        soilMoisture: data.node_soil_moisture_percent_2,
        soilTemperature: data.node_DS18B20_temperature,
        rainDropIntensity: data.node_rain_percent,
      });
    });

    return () => {
      channel.unbind_all();
      channel.unsubscribe();
    };
  }, []);

  return (
    <div className="p-4">
      <Tab.Group selectedIndex={activeTab === 'base' ? 0 : 1} onChange={(index) => setActiveTab(index === 0 ? 'base' : 'child')}>
        <Tab.List className="flex space-x-1 rounded-xl bg-green-500 p-1">
          <Tab className={({ selected }) => `w-full py-2.5 text-sm font-medium text-blue-700 rounded-lg ${selected ? 'bg-white shadow' : 'text-blue-100'}`}>Base Node</Tab>
          <Tab className={({ selected }) => `w-full py-2.5 text-sm font-medium text-blue-700 rounded-lg ${selected ? 'bg-white shadow' : 'text-blue-100'}`}>Child Node</Tab>
        </Tab.List>
        <Tab.Panels>
          <Tab.Panel>
            <h2 className="text-lg font-bold">Base Node Sensor Data</h2>
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <CardDataStats title="Atmospheric Pressure" total={`${baseNodeData.atmosphericPressure ?? 'N/A'} hPa`} />
              <CardDataStats title="Solar Intensity" total={`${baseNodeData.solarIntensity ?? 'N/A'} W/m²`} />
              <CardDataStats title="Humidity" total={`${baseNodeData.humidity ?? 'N/A'}%`} />
              <CardDataStats title="Temperature" total={`${baseNodeData.temperature ?? 'N/A'}°C`} />
              <CardDataStats title="Soil Moisture" total={`${baseNodeData.soilMoisture ?? 'N/A'}%`} />
              <CardDataStats title="Ambient Light Color" total={`RGB(${baseNodeData.ambientLight?.r ?? 0}, ${baseNodeData.ambientLight?.g ?? 0}, ${baseNodeData.ambientLight?.b ?? 0})`} />
              <CardDataStats title="Gas Sensor MQ-2" total={baseNodeData.gasSensors?.mq2 ?? 'N/A'} />
              <CardDataStats title="Gas Sensor MQ-135" total={baseNodeData.gasSensors?.mq135 ?? 'N/A'} />
              <CardDataStats title="Relay State" total={baseNodeData.relayState ?? 'N/A'} />
              <CardDataStats title="Water Flow Rate" total={`${baseNodeData.waterFlowRate ?? 'N/A'} L/min`} />
            </div>
            <div className="mt-4">
              <h3>Humidity and Temperature</h3>
              <ChartOne series={[{ name: 'Humidity', data: [baseNodeData.humidity ?? 0] }, { name: 'Temperature', data: [baseNodeData.temperature ?? 0] }]} />
            </div>
            <div className="mt-4">
              <h3>Water Flow Rate</h3>
              <ChartOne series={[{ name: 'Water Flow Rate', data: [baseNodeData.waterFlowRate ?? 0] }]} />
            </div>
          </Tab.Panel>
          <Tab.Panel>
            <h2 className="text-lg font-bold">Child Node Sensor Data</h2>
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <CardDataStats title="Humidity" total={`${childNodeData.humidity ?? 'N/A'}%`} />
              <CardDataStats title="Soil Moisture" total={`${childNodeData.soilMoisture ?? 'N/A'}%`} />
              <CardDataStats title="Soil Temperature" total={`${childNodeData.soilTemperature ?? 'N/A'}°C`} />
              <CardDataStats title="Rain Drop Intensity" total={`${childNodeData.rainDropIntensity ?? 'N/A'} mm`} />
            </div>
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
};

export default SensorDashboard;