"use client";

import { useState } from "react";

type Meeting = {
  id: string;
  summary: string;
  action_items: { task: string; status: string; owners: string[]; due_dates: string[] }[];
  decisions: { decision: string }[];
};

export default function MeetingDetailsPage({ params }: { params: { id: string } }) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<string>("");
  const [meeting, setMeeting] = useState<Meeting | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type !== "audio/mpeg") {
        alert("Please upload a valid MP3 file.");
        return;
      }
      setFile(selectedFile);
      setMessage("");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setMessage("");
    setMeeting(null);

    try {
      // Upload file and team id using POST request
      const formData = new FormData();
      formData.append("team", params.id);
      formData.append("audio_file", file);

      const uploadRes = await fetch("http://localhost:8000/process-meeting/", {
        method: "POST",
        body: formData,
      });

      const uploadData = await uploadRes.json();

      if (!uploadRes.ok) {
        setMessage(`❌ Upload failed: ${uploadData.detail || "Unknown error"}`);
        setUploading(false);
        return;
      }

      setMessage("✅ File uploaded and meeting processed successfully!");

      // Fetch meetings array for the team using GET
      const meetingsRes = await fetch(`http://localhost:8000/meetings/${params.id}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (!meetingsRes.ok) {
        setMessage("❌ Failed to fetch meeting details.");
        setUploading(false);
        return;
      }

      const meetingsData: Meeting[] = await meetingsRes.json();

      if (meetingsData.length > 0) {
        // Display the most recent meeting (first in array)
        setMeeting(meetingsData[0]);
      } else {
        setMessage("ℹ️ No meetings found for this team.");
      }
    } catch (error) {
      console.error("Upload or fetch error:", error);
      setMessage("❌ An error occurred while uploading or fetching meeting data.");
    } finally {
      setUploading(false);
      setFile(null);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] bg-gray-900 text-gray-100 px-6 py-12">
      <h1 className="text-4xl md:text-5xl font-bold text-indigo-400 mb-8 text-center">
        Upload Meeting Audio 📝
      </h1>

      <div className="bg-gray-800 p-8 rounded-2xl shadow-xl w-full max-w-2xl">
        <label className="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed border-indigo-500 rounded-lg cursor-pointer hover:bg-gray-700 transition">
          <span className="text-gray-300">
            {file ? `Selected: ${file.name}` : "Click to upload or drag & drop MP3"}
          </span>
          <input type="file" accept=".mp3" className="hidden" onChange={handleFileChange} />
        </label>

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="mt-6 bg-indigo-500 hover:bg-indigo-600 px-4 py-2 rounded-lg disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload & Process"}
        </button>

        {message && <p className="mt-4 text-green-400">{message}</p>}

        {meeting && (
          <div className="mt-6">
            <h3 className="text-xl font-bold text-indigo-300 mb-2">Summary</h3>
            <p className="text-gray-300 bg-gray-700 p-4 rounded-lg">{meeting.summary}</p>

            <h3 className="text-xl font-bold text-purple-300 mt-6 mb-2">Action Items</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-300">
              {meeting.action_items.map((item, idx) => (
                <li key={idx}>
                  {item.task} — {item.status} (Owners: {item.owners.join(", ")}, Due: {item.due_dates.join(", ")})
                </li>
              ))}
            </ul>

            <h3 className="text-xl font-bold text-green-300 mt-6 mb-2">Decisions</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-300">
              {meeting.decisions.map((d, idx) => (
                <li key={idx}>{d.decision}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
