function ConfirmModal({
  open,
  title,
  message,
  confirmText = "Delete",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
}) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm">

      <div className="card-bg rounded-2xl p-6 w-[420px] shadow-2xl">

        <h2 className="text-2xl font-bold text-theme">
          {title}
        </h2>

        <p className="text-theme opacity-70 mt-3">
          {message}
        </p>

        <div className="flex justify-end gap-3 mt-8">

          <button
            onClick={onCancel}
            className="px-5 py-2 rounded-lg border-theme"
          >
            {cancelText}
          </button>

          <button
            onClick={onConfirm}
            className="bg-red-500 hover:bg-red-600 text-white px-5 py-2 rounded-lg"
          >
            {confirmText}
          </button>

        </div>

      </div>

    </div>
  );
}

export default ConfirmModal;