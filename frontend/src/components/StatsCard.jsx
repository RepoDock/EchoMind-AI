function StatsCard({ title, value }) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-lg transition hover:border-cyan-400 hover:shadow-cyan-500/10">
      <p className="text-sm text-slate-400">{title}</p>

      <h2 className="mt-3 text-4xl font-bold text-white">
        {value}
      </h2>
    </div>
  );
}

export default StatsCard;