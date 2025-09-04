import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { 
  CloudArrowUpIcon, 
  DocumentTextIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline';

interface UploadedDocument {
  id: string;
  filename: string;
  uploadDate: string;
  status: 'processing' | 'completed' | 'error';
  fileSize: number;
  ocr_text?: string;
  extracted_keywords?: string[];
  processing_complete?: boolean;
}

interface MatchedProvider {
  id: number;
  name: string;
  specialty: string;
  location: string;
  match_score: number;
  matched_keywords: string[];
}

const DocumentUpload: React.FC = () => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [matchedProviders, setMatchedProviders] = useState<MatchedProvider[]>([]);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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

  const handleFiles = async (files: FileList) => {
    const file = files[0];
    
    if (!file.type.startsWith('image/') && file.type !== 'application/pdf') {
      setUploadError('Please upload an image or PDF file');
      return;
    }

    setUploading(true);
    setUploadError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/api/v1/documents/upload-file`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const newDocument: UploadedDocument = {
        id: Date.now().toString(),
        filename: file.name,
        uploadDate: new Date().toISOString(),
        status: 'completed',
        fileSize: file.size,
        ocr_text: response.data.document.ocr_text,
        extracted_keywords: response.data.document.extracted_keywords,
        processing_complete: response.data.document.processing_complete
      };

      setDocuments(prev => [newDocument, ...prev]);

      if (response.data.matched_providers) {
        setMatchedProviders(response.data.matched_providers);
      }

    } catch (error) {
      console.error('Upload error:', error);
      setUploadError('Failed to upload and process document. Please try again.');
      
      const errorDocument: UploadedDocument = {
        id: Date.now().toString(),
        filename: file.name,
        uploadDate: new Date().toISOString(),
        status: 'error',
        fileSize: file.size
      };
      setDocuments(prev => [errorDocument, ...prev]);
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Document Upload</h1>
        <p className="mt-2 text-gray-600">
          Upload medical documents for OCR processing and provider matching
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <div
          className={`relative border-2 border-dashed rounded-lg p-6 ${
            dragActive 
              ? 'border-primary-500 bg-primary-50' 
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-upload"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={handleChange}
            accept="image/*,.pdf"
            disabled={uploading}
          />
          
          <div className="text-center">
            <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
            <div className="mt-4">
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="mt-2 block text-sm font-medium text-gray-900">
                  {uploading ? 'Processing...' : 'Drop files here or click to upload'}
                </span>
              </label>
              <p className="mt-2 text-xs text-gray-500">
                PNG, JPG, GIF, PDF up to 10MB
              </p>
            </div>
          </div>
        </div>

        {uploadError && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <div className="flex">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
              <div className="ml-3">
                <p className="text-sm text-red-800">{uploadError}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {matchedProviders.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center mb-4">
            <MagnifyingGlassIcon className="h-6 w-6 text-primary-600 mr-2" />
            <h2 className="text-lg font-medium text-gray-900">
              Recommended Healthcare Providers
            </h2>
          </div>
          <p className="text-sm text-gray-600 mb-4">
            Based on the content of your uploaded document, we found these matching providers:
          </p>
          
          <div className="space-y-4">
            {matchedProviders.map((provider, index) => (
              <div key={provider.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">{provider.name}</h3>
                    <p className="text-sm text-gray-600">{provider.specialty}</p>
                    <p className="text-sm text-gray-500">{provider.location}</p>
                    
                    {provider.matched_keywords.length > 0 && (
                      <div className="mt-2">
                        <p className="text-xs text-gray-500 mb-1">Matched Keywords:</p>
                        <div className="flex flex-wrap gap-1">
                          {provider.matched_keywords.map((keyword, idx) => (
                            <span
                              key={idx}
                              className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
                            >
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="ml-4 text-right">
                    <div className="text-lg font-bold text-primary-600">
                      {Math.round(provider.match_score * 100)}%
                    </div>
                    <div className="text-xs text-gray-500">Match</div>
                  </div>
                </div>
                
                <div className="mt-3 flex space-x-3">
                  <button className="text-sm text-primary-600 hover:text-primary-500 font-medium">
                    View Profile
                  </button>
                  <button className="text-sm text-primary-600 hover:text-primary-500 font-medium">
                    Book Appointment
                  </button>
                  <button className="text-sm text-gray-600 hover:text-gray-500 font-medium">
                    Contact
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {documents.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Uploaded Documents ({documents.length})
            </h3>
            
            <div className="space-y-4">
              {documents.map((doc) => (
                <div key={doc.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <DocumentTextIcon className="h-8 w-8 text-gray-400" />
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">{doc.filename}</h4>
                        <p className="text-sm text-gray-500">
                          {formatDate(doc.uploadDate)} • {formatFileSize(doc.fileSize)}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      {doc.status === 'completed' && (
                        <CheckCircleIcon className="h-5 w-5 text-green-500" />
                      )}
                      {doc.status === 'error' && (
                        <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
                      )}
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        doc.status === 'completed' ? 'bg-green-100 text-green-800' :
                        doc.status === 'error' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {doc.status.charAt(0).toUpperCase() + doc.status.slice(1)}
                      </span>
                    </div>
                  </div>
                  
                  {doc.extracted_keywords && doc.extracted_keywords.length > 0 && (
                    <div className="mt-3">
                      <p className="text-xs text-gray-500 mb-2">Extracted Keywords:</p>
                      <div className="flex flex-wrap gap-1">
                        {doc.extracted_keywords.map((keyword, idx) => (
                          <span
                            key={idx}
                            className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {doc.ocr_text && (
                    <div className="mt-3">
                      <p className="text-xs text-gray-500 mb-2">Extracted Text (Preview):</p>
                      <div className="bg-gray-50 rounded-md p-3">
                        <p className="text-sm text-gray-700 line-clamp-3">
                          {doc.ocr_text.substring(0, 200)}
                          {doc.ocr_text.length > 200 ? '...' : ''}
                        </p>
                      </div>
                    </div>
                  )}
                  
                  <div className="mt-3 flex space-x-3">
                    <button className="text-sm text-primary-600 hover:text-primary-500 font-medium">
                      View Full Text
                    </button>
                    <button className="text-sm text-primary-600 hover:text-primary-500 font-medium">
                      Download
                    </button>
                    <button className="text-sm text-gray-600 hover:text-gray-500 font-medium">
                      Delete
                    </button>
                  </div>
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
