import PatientRow from '@components/patients/PatientRow';
import EmptyState from '@components/patients/ui/EmptyState';
import ErrorState from '@components/patients/ui/ErrorState';
import LoadingState from '@components/patients/ui/LoadingState';
import { usePatients } from '@queries/patient';
import { useState } from 'react';

const PatientList = () => {
  const [searchName, setSearchName] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // Use React Query to fetch patients data
  const { data, isLoading, isError, error, refetch } = usePatients(
    searchQuery ? { name: searchQuery } : undefined
  );

  const handleSearch = () => {
    setSearchQuery(searchName);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  if (isLoading) return <LoadingState />;

  if (isError)
    return (
      <ErrorState
        message={`Failed to load patients: ${error instanceof Error ? error.message : 'Unknown error'}`}
        onRetry={() => refetch()}
      />
    );

  if (!data || !data.patients || data.patients.length === 0) return <EmptyState />;

  return (
    <div className="w-full overflow-hidden">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Patient List</h2>

        <div className="flex flex-row gap-2 flex-wrap">
          <input
            type="text"
            placeholder="Search patients by name..."
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            onKeyDown={handleKeyDown}
            className="px-3 py-1.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 flex-grow text-sm"
            aria-label="Search patients"
          />
          <button
            onClick={handleSearch}
            className="px-3 py-1.5 bg-gray-100 text-gray-700 text-sm font-medium rounded hover:bg-gray-200 transition-colors whitespace-nowrap"
            aria-label="Search button"
          >
            Search
          </button>
          <button
            className="px-3 py-1.5 bg-blue-500 text-white text-sm font-medium rounded hover:bg-blue-600 transition-colors whitespace-nowrap"
            aria-label="Add a new patient"
          >
            Add Patient
          </button>
        </div>
      </div>

      <div className="w-full bg-white shadow-md rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Name
                </th>
                <th
                  scope="col"
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell"
                >
                  DOB
                </th>
                <th
                  scope="col"
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell"
                >
                  ID
                </th>
                <th
                  scope="col"
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell"
                >
                  Resource Type
                </th>
                <th
                  scope="col"
                  className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.patients.map((patient) => (
                <PatientRow key={patient.id} patient={patient} />
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mt-4 gap-2">
        <div className="text-sm text-gray-700">
          Showing <span className="font-medium">{data.patients.length}</span> patient(s)
        </div>
      </div>
    </div>
  );
};

export default PatientList;
