import { Patient } from '@queries/patient';

interface PatientRowProps {
  patient: Patient;
}

const PatientRow = ({ patient }: PatientRowProps) => {
  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <tr className="hover:bg-gray-50">
      <td className="px-4 py-3 whitespace-nowrap">
        <div className="text-sm font-medium text-gray-900">{patient.full_name}</div>
      </td>
      <td className="px-4 py-3 whitespace-nowrap hidden sm:table-cell">
        <div className="text-sm text-gray-500">{formatDate(patient.birth_date)}</div>
      </td>
      <td className="px-4 py-3 whitespace-nowrap hidden md:table-cell">
        <div className="text-sm text-gray-500">{patient.id}</div>
      </td>
      <td className="px-4 py-3 whitespace-nowrap hidden lg:table-cell">
        <div className="text-sm text-gray-500">{patient.resourceType}</div>
      </td>
      <td className="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
        <button
          className="text-blue-600 hover:text-blue-900 mr-2"
          aria-label={`View ${patient.full_name}`}
        >
          View
        </button>
        <button
          className="text-blue-600 hover:text-blue-900 mr-2"
          aria-label={`Edit ${patient.full_name}`}
        >
          Edit
        </button>
        <button className="text-red-600 hover:text-red-900" aria-label={`Delete ${patient.full_name}`}>
          Delete
        </button>
      </td>
    </tr>
  );
};

export default PatientRow;
