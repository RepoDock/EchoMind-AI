
function StatsCard({ title, value }) {
  return (
    <div className="card-bg rounded-2xl p-6">
      <h3 className="text-theme opacity-70 text-lg">
        {title}
      </h3>

      <h1 className="text-5xl font-bold text-theme mt-4">
        {value}
      </h1>
    </div>
  );
}

export default StatsCard;