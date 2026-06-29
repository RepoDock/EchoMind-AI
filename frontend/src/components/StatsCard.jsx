
function StatsCard({ title, value }) {
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6">
      <h3 className="text-slate-400 text-lg">
        {title}
      </h3>

      <h1 className="text-5xl font-bold text-white mt-4">
        {value}
      </h1>
    </div>
  );
}

export default StatsCard;