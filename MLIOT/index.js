const React = require('react');
const { useState, useEffect } = React;
const SerialPort = require('serialport');
const Readline = require('@serialport/parser-readline');

const App = () => {
  const [data, setData] = useState('');
  const [points, setPoints] = useState(0);  

  useEffect(() => {
    const port = new SerialPort('/dev/cu.usbmodemFA141', { baudRate: 9600 });
    const parser = port.pipe(new Readline({ delimiter: '\n' }));

    port.on('open', () => {
      console.log('Serial port open');
    });

    parser.on('data', (serialData) => {
      console.log(`Received data: ${serialData}`);
      
      const weight = parseFloat(serialData.trim());
      if (!isNaN(weight)) {
        setData(weight); 
        const calculatedPoints = weight * 10; 
        setPoints(calculatedPoints); // Update points
      }
    });

    return () => {
      port.close((err) => {
        if (err) console.error('Error closing port', err);
        else console.log('Serial port closed');
      });
    };
  }, []); // Empty array ensures this effect runs only once

  return (
    <div className="App">
      <p>Weight of Waste: {data} kg</p>
      <p>User Points: {points}</p>
    </div>
  );
};

module.exports = App;


