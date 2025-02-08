import { useState } from 'react';
import { format } from 'date-fns';
import dayjs from 'dayjs';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { StaticTimePicker } from '@mui/x-date-pickers/StaticTimePicker';

export default function IrrigationPage() {
  const [relayOn, setRelayOn] = useState(false);
  const [startTime, setStartTime] = useState(Date.now());
  const [duration, setDuration] = useState(30);
  const [flowRate, setFlowRate] = useState(10);
  const [individualUsage, setIndividualUsage] = useState(300);
  const [totalMeasurementDuration, setTotalMeasurementDuration] = useState(600);
  const [totalWaterUsage, setTotalWaterUsage] = useState(5000);

  const lastIrrigation = new Date();
  const irrigationTimes = ['06:00', '12:00', '18:00'];

  const upcomingIrrigation = irrigationTimes.map((time) => {
    const date = new Date();
    date.setHours(parseInt(time.split(':')[0]), parseInt(time.split(':')[1]));
    return date;
  });

  const currentDate = new Date();
  const currentDay = currentDate.toLocaleDateString('en-US', {
    weekday: 'long',
  });
  return (
    <div className="p-8 bg-gray-100 min-h-screen flex flex-col items-center">
      <h1 className="text-4xl font-bold mb-6 text-gray-800">
        Irrigation Control Panel
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-6xl">
        {/* Relay Status */}
        <div className="p-6 bg-white shadow-lg rounded-xl w-full">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xl font-semibold">Relay Status</span>
            <input
              type="checkbox"
              checked={relayOn}
              onChange={() => setRelayOn(!relayOn)}
              className="toggle-checkbox"
            />
          </div>
          <p className="text-gray-600 text-sm">
            Toggle the relay to manually start or stop the irrigation system.
          </p>
          {/* <p>{Date.now()}</p> */}

          <p className="text-sm text-gray-600">
            <strong>Date:</strong> {format(currentDate, 'PPpp')}
          </p>
          <p className="text-sm text-gray-600">
            <strong>Day:</strong> {currentDay}
          </p>
        </div>

        {/* Irrigation Cycle */}
        <div className="p-6 bg-white shadow-lg rounded-xl w-full">
          <span className="text-xl font-semibold">Irrigation Cycle</span>
          <p className="text-gray-600 text-sm mb-3">
            Set the start time and duration for the irrigation cycle.
          </p>

          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DemoContainer components={['StaticTimePicker']}>
              <DemoItem label="Static variant">
                <StaticTimePicker defaultValue={dayjs(startTime)} />
              </DemoItem>
            </DemoContainer>
          </LocalizationProvider>

          <p>Start Time : {startTime}</p>

          <div className="mt-2">
            <label className="block text-sm text-gray-600">
              Duration (min)
            </label>
            <input
              type="range"
              min="1"
              max="120"
              step="1"
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="w-full"
            />
            <span className="block mt-1 text-sm">{duration} min</span>
          </div>
        </div>

        {/* Last Irrigation & Upcoming Cycles */}
        <div className="p-6 bg-white shadow-lg rounded-xl w-full">
          <span className="text-xl font-semibold">Irrigation Schedule</span>
          <p className="text-gray-600 text-sm mb-3">
            Track the last irrigation and upcoming scheduled cycles.
          </p>
          <p className="text-sm text-gray-600">
            <strong>Last Irrigation:</strong> {format(lastIrrigation, 'PPpp')}
          </p>
          {upcomingIrrigation.map((time, index) => (
            <p key={index} className="text-sm text-gray-600">
              <strong>Upcoming:</strong> {format(time, 'PPpp')}
            </p>
          ))}
        </div>

        {/* Water Consumption */}
        <div className="p-6 bg-white shadow-lg rounded-xl w-full">
          <span className="text-xl font-semibold">Water Consumption</span>
          <p className="text-gray-600 text-sm mb-3">
            Real-time data on water usage and flow rate.
          </p>
          <p className="text-sm text-gray-600">
            💧 Flow Rate: {flowRate} L/min
          </p>
          <p className="text-sm text-gray-600">
            🚰 Individual Usage: {individualUsage} L
          </p>
          <p className="text-sm text-gray-600">
            ⏳ Total Duration: {totalMeasurementDuration} sec
          </p>
          <p className="text-lg font-semibold text-gray-600">
            🔹Total Water Used: {totalWaterUsage} L
          </p>
        </div>

        {/* Calendar for Multi-Irrigation */}
        <div className="p-6 bg-white shadow-lg rounded-xl col-span-1 md:col-span-2 w-full">
          <span className="text-xl font-semibold">
            Irrigation Schedule Calendar
          </span>
          <p className="text-gray-600 text-sm mb-3">
            View past and upcoming irrigation cycles. Multiple irrigations per
            day are highlighted.
          </p>
        </div>
      </div>
    </div>
  );
}
