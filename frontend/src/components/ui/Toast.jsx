function Toast({
  show,
  message,
  type = "success",
}) {
  if (!show) return null;

  return (
    <div className="fixed top-6 right-6 z-[200]">

      <div
        className={`px-5 py-4 rounded-xl shadow-xl text-white font-medium
        ${
          type === "success"
            ? "bg-green-600"
            : "bg-red-600"
        }`}
      >
        {message}
      </div>

    </div>
  );
}

export default Toast;