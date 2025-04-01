interface ErrorStateProps {
  message: string;
  onRetry: () => void;
}

const ErrorState = ({ message, onRetry }: ErrorStateProps) => (
  <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-700">
    <p>{message}</p>
    <button
      className="mt-2 px-4 py-2 bg-red-100 text-red-700 font-medium rounded hover:bg-red-200 transition-colors"
      onClick={onRetry}
    >
      Retry
    </button>
  </div>
);

export default ErrorState;
