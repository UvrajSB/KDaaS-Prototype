export function Textarea({ value, onChange, placeholder }) {
    return (
      <textarea
        className="border rounded px-3 py-2 w-full"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
      />
    );
  }
  