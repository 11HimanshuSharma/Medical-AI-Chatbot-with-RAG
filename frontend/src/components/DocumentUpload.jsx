import React, { useState } from 'react';
import { Upload, FileText, X, CheckCircle } from 'lucide-react';

export const DocumentUpload = ({ onUpload, uploadedDocs = [] }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files).filter(file => 
      file.type === 'application/pdf' || file.name.endsWith('.pdf')
    );
    if (files.length > 0) {
      await handleUpload(files);
    }
  };

  const handleFileSelect = async (e) => {
    const files = Array.from(e.target.files).filter(file => 
      file.type === 'application/pdf' || file.name.endsWith('.pdf')
    );
    if (files.length > 0) {
      await handleUpload(files);
    }
  };

  const handleUpload = async (files) => {
    setUploading(true);
    for (const file of files) {
      await onUpload(file);
    }
    setUploading(false);
  };

  return (
    <div className="border-b border-gray-200 bg-white p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-gray-700">Medical Documents</h3>
          <span className="text-xs text-gray-500">{uploadedDocs.length} documents uploaded</span>
        </div>

        {/* Upload Area */}
        <div
          className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
            isDragging
              ? 'border-blue-400 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            type="file"
            multiple
            accept=".pdf"
            onChange={handleFileSelect}
            className="hidden"
            id="file-upload"
          />
          
          {uploading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              <span className="ml-2 text-sm text-gray-600">Uploading...</span>
            </div>
          ) : (
            <>
              <Upload className="mx-auto h-8 w-8 text-gray-400 mb-2" />
              <div className="text-sm text-gray-600">
                <label htmlFor="file-upload" className="cursor-pointer">
                  <span className="text-blue-600 hover:text-blue-500">Upload medical PDFs</span>
                  <span> or drag and drop</span>
                </label>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Treatment guidelines, research papers, drug sheets, lab documentation
              </p>
            </>
          )}
        </div>

        {/* Uploaded Documents List */}
        {uploadedDocs.length > 0 && (
          <div className="mt-4">
            <div className="grid gap-2 max-h-32 overflow-y-auto">
              {uploadedDocs.map((doc, index) => (
                <div key={index} className="flex items-center justify-between bg-gray-50 rounded-lg p-2">
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <FileText className="h-4 w-4 text-gray-500 flex-shrink-0" />
                    <span className="text-sm text-gray-700 truncate">{doc.name}</span>
                    <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                  </div>
                  <div className="text-xs text-gray-500">
                    {(doc.size / 1024 / 1024).toFixed(1)}MB
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
