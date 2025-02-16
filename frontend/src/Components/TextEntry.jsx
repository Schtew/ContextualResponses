import React, { useState } from 'react';
import { Send } from 'lucide-react';

const TextEntry = () => {
  const [input, setInput] = useState('');
  const [toggles, setToggles] = useState({
    Wikipedia: false,
    Stackoverflow: false,
    arXiv: false
  });

  const handleToggle = (name) => {
    setToggles(prev => ({
      ...prev,
      [name]: !prev[name]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', input, toggles);
    setInput('');
  };

  return (
    <div style={{
      width: '70%',
      padding: '2vh',
      backgroundColor: 'white',
      borderRadius: '15px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      margin: '2vh auto',
      marginTop: '30vh'
    }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '2vh' }}>
        <div style={{ 
          display: 'flex', 
          gap: '2vw', 
          alignItems: 'center',
          justifyContent: 'center',
          padding: '1vh'
        }}>
          {Object.entries(toggles).map(([name, checked]) => (
            <label key={name} style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.5vw',
              fontSize: '2.5vh',
              color: '#9a2424',
              cursor: 'pointer'
            }}>
              <input
                type="checkbox"
                checked={checked}
                onChange={() => handleToggle(name)}
                style={{ 
                  width: '2vh',
                  height: '2vh',
                  cursor: 'pointer'
                }}
              />
              <span>
                {name}
              </span>
            </label>
          ))}
        </div>

        <div style={{ 
          display: 'flex', 
          gap: '1vw', 
          alignItems: 'center',
          padding: '1vh'
        }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything..."
            style={{
              flex: 1,
              padding: '2vh',
              fontSize: '2.5vh',
              backgroundColor: '#f6ebdf',
              border: 'none',
              borderRadius: '10px',
              outline: 'none',
              color: '#9a2424'
            }}
          />
          <button
            type="submit"
            style={{
              padding: '2vh',
              backgroundColor: '#cf5c49',
              border: 'none',
              borderRadius: '10px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background-color 0.3s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#9a2424'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#cf5c49'}
          >
            <Send color="white" size={24} />
          </button>
        </div>
      </form>
    </div>
  );
};

export default TextEntry;