import React from 'react';

const SWOT_CONFIG = {
  strengths: {
    title: 'Strengths',
    icon: '💪',
  },
  weaknesses: {
    title: 'Weaknesses',
    icon: '⚠️',
  },
  opportunities: {
    title: 'Opportunities',
    icon: '🚀',
  },
  threats: {
    title: 'Threats',
    icon: '🛡️',
  },
};

function SwotCard({ type, items }) {
  const config = SWOT_CONFIG[type];
  if (!config) return null;

  const itemList = Array.isArray(items) ? items : ['Not available'];

  return (
    <div className={`swot-card ${type}`} id={`swot-${type}`}>
      <h4>
        <span>{config.icon}</span>
        {config.title}
      </h4>
      <ul>
        {itemList.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function SwotGrid({ swotData }) {
  if (!swotData) return null;

  return (
    <div className="swot-grid stagger-children">
      <SwotCard type="strengths" items={swotData.strengths} />
      <SwotCard type="weaknesses" items={swotData.weaknesses} />
      <SwotCard type="opportunities" items={swotData.opportunities} />
      <SwotCard type="threats" items={swotData.threats} />
    </div>
  );
}

export { SwotCard, SwotGrid };
export default SwotGrid;
