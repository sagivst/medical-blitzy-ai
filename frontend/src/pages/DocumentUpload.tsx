import React, { useState, useCallback } from 'react';
import { 
  CloudArrowUpIcon, 
  DocumentTextIcon, 
  PhotoIcon,
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  status: 'uploading' | 'processing' | 'completed' | 'error';
  progress: number;
  ocrResult?: string;
  fhirData?: any;
  matchedProviders?: any[];
}

const DocumentUpload: React.FC = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = (fileList: FileList) => {
    const newFiles: UploadedFile[] = Array.from(fileList).map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'uploading',
      progress: 0
    }));

    setFiles(prev => [...prev, ...newFiles]);

    newFiles.forEach(file => {
      const actualFile = Array.from(fileList).find(f => f.name === file.name);
      if (actualFile) {
        uploadToBackend(actualFile, file.id);
      }
    });
  };

  const uploadToBackend = async (file: File, fileId: string) => {
    try {
      setFiles(prev => prev.map(f => {
        if (f.id === fileId) {
          return { ...f, status: 'processing' };
        }
        return f;
      }));

      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('http://localhost:8000/api/v1/documents/upload-file', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }
      
      const result = await response.json();
      console.log('Backend response:', result);
      
      setFiles(prev => prev.map(f => {
        if (f.id === fileId) {
          return {
            ...f,
            status: 'completed',
            ocrResult: result.document?.ocr_text || 'No OCR text available',
            fhirData: result.document,
            matchedProviders: result.matched_providers || []
          };
        }
        return f;
      }));
      
    } catch (error) {
      console.error('Upload failed:', error);
      setFiles(prev => prev.map(f => {
        if (f.id === fileId) {
          return { ...f, status: 'error' };
        }
        return f;
      }));
    }
  };

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'error':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      default:
        return <div className="h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Document Upload</h1>
        <p className="mt-2 text-gray-600">
          Upload medical documents for OCR processing and FHIR conversion
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <div
          className={`relative border-2 border-dashed rounded-lg p-6 ${
            dragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="text-center">
            <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
            <div className="mt-4">
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="mt-2 block text-sm font-medium text-gray-900">
                  Drop files here or click to upload
                </span>
                <input
                  id="file-upload"
                  name="file-upload"
                  type="file"
                  className="sr-only"
                  multiple
                  accept=".pdf,.jpg,.jpeg,.png,.tiff,.doc,.docx"
                  onChange={handleChange}
                />
              </label>
              <p className="mt-2 text-xs text-gray-500">
                Supported formats: PDF, JPG, PNG, TIFF, DOC, DOCX up to 10MB
              </p>
            </div>
          </div>
        </div>
      </div>

      {files.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Uploaded Documents ({files.length})
            </h3>
            <div className="space-y-4">
              {files.map((file) => (
                <div key={file.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="flex-shrink-0">
                        {file.type.startsWith('image/') ? (
                          <PhotoIcon className="h-8 w-8 text-gray-400" />
                        ) : (
                          <DocumentTextIcon className="h-8 w-8 text-gray-400" />
                        )}
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {file.name}
                        </p>
                        <p className="text-sm text-gray-500">
                          {formatFileSize(file.size)} • {file.status}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(file.status)}
                      <button
                        onClick={() => removeFile(file.id)}
                        className="text-gray-400 hover:text-gray-500"
                      >
                        <XMarkIcon className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                  
                  {file.status === 'uploading' && (
                    <div className="mt-2">
                      <div className="bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${file.progress}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {file.status === 'processing' && (
                    <div className="mt-2 text-sm text-blue-600">
                      Processing with OCR and converting to FHIR format...
                    </div>
                  )}

                  {file.status === 'completed' && file.ocrResult && (
                    <div className="mt-3 p-3 bg-green-50 rounded-md">
                      <h4 className="text-sm font-medium text-green-800 mb-2">
                        OCR Processing Complete
                      </h4>
                      <p className="text-sm text-green-700 mb-2">
                        Extracted text preview:
                      </p>
                      <p className="text-xs text-green-600 bg-white p-2 rounded border">
                        {file.ocrResult.substring(0, 200)}...
                      </p>
                      <div className="mt-2 flex space-x-2">
                        <button className="text-xs bg-green-600 text-white px-2 py-1 rounded hover:bg-green-700">
                          View Full Text
                        </button>
                        <button className="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700">
                          View FHIR Data
                        </button>
                      </div>
                    </div>
                  )}

                  {file.status === 'completed' && file.matchedProviders && file.matchedProviders.length > 0 && (
                    <div className="mt-3 p-3 bg-blue-50 rounded-md">
                      <h4 className="text-sm font-medium text-blue-800 mb-2">
                        Recommended Providers ({file.matchedProviders.length})
                      </h4>
                      <div className="space-y-2">
                        {file.matchedProviders.slice(0, 3).map((provider, index) => (
                          <div key={index} className="text-sm bg-white p-2 rounded border">
                            <div className="font-medium text-blue-900">{provider.name}</div>
                            <div className="text-blue-700">{provider.specialty} • {provider.location}</div>
                            <div className="text-blue-600">Match Score: {Math.round(provider.match_score * 100)}%</div>
                            <div className="text-xs text-blue-500">
                              Keywords: {provider.matched_keywords?.join(', ')}
                            </div>
                          </div>
                        ))}
                      </div>
                      <div className="mt-2">
                        <button className="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700">
                          View All Providers
                        </button>
                      </div>
                    </div>
                  )}

                  {file.status === 'error' && (
                    <div className="mt-2 text-sm text-red-600">
                      Error processing document. Please try again.
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
