export function Button({ children, onClick, disabled }) {
    return (
      <button
        className={`px-4 py-2 mt-6 bg-blue-600 text-white rounded ${
          disabled ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-700"
        }`}
        onClick={onClick}
        disabled={disabled}
      >
        {children}
      </button>
    );
  }
  