export type NodeType = 'base' | 'child';

export interface Feature {
  id: string;
  name: string;
  description: string;
}

export interface Sensor {
  id: string;
  name: string;
  description: string;
  price: number;
  features: Feature[];
  nodeType?: NodeType;
}

export const sensors: Sensor[] = [
  {
    id: 'temp',
    name: 'Temperature Sensor',
    description: 'Monitor ambient temperature with high precision',
    price: 100,
    features: [
      {
        id: 'temp1',
        name: 'Real-time temperature tracking',
        description: 'Get up-to-the-minute temperature data',
      },
      {
        id: 'temp2',
        name: 'Temperature alerts',
        description: 'Set custom alerts for temperature thresholds',
      },
      {
        id: 'temp3',
        name: 'Historical temperature data',
        description: 'Access and analyze past temperature trends',
      },
    ],
  },
  {
    id: 'humid',
    name: 'Humidity Sensor',
    description: 'Track humidity levels for optimal comfort',
    price: 100,
    features: [
      {
        id: 'humid1',
        name: 'Real-time humidity tracking',
        description: 'Monitor current humidity levels',
      },
      {
        id: 'humid2',
        name: 'Mold risk alerts',
        description: 'Receive warnings about potential mold growth conditions',
      },
      {
        id: 'humid3',
        name: 'Historical humidity data',
        description: 'View humidity trends over time',
      },
    ],
  },
  {
    id: 'motion',
    name: 'Motion Sensor',
    description: 'Detect movement in your space',
    price: 150,
    features: [
      {
        id: 'motion1',
        name: 'Motion-triggered alerts',
        description: 'Get notified when motion is detected',
      },
      {
        id: 'motion2',
        name: 'Activity heatmaps',
        description: 'Visualize movement patterns in your space',
      },
      {
        id: 'motion3',
        name: 'Customizable sensitivity',
        description: 'Adjust motion detection sensitivity',
      },
    ],
  },
  {
    id: 'light',
    name: 'Light Sensor',
    description: 'Measure and respond to ambient light levels',
    price: 200,
    features: [
      {
        id: 'light1',
        name: 'Daylight tracking',
        description: 'Monitor natural light levels throughout the day',
      },
      {
        id: 'light2',
        name: 'Energy-saving recommendations',
        description: 'Get tips to optimize lighting and save energy',
      },
      {
        id: 'light3',
        name: 'Light-based automation triggers',
        description: 'Set up automated actions based on light levels',
      },
    ],
  },
  {
    id: 'air',
    name: 'Air Quality Sensor',
    description: 'Monitor air quality for a healthier environment',
    price: 260,
    features: [
      {
        id: 'air1',
        name: 'Real-time air quality monitoring',
        description: 'Track current air quality index',
      },
      {
        id: 'air2',
        name: 'Pollution alerts',
        description: 'Receive notifications about poor air quality',
      },
      {
        id: 'air3',
        name: 'Air quality history and trends',
        description: 'Analyze air quality patterns over time',
      },
    ],
  },
];
