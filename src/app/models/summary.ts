import mongoose, { Schema, Document, models } from "mongoose";

export interface ISummary extends Document {
  team: string;
  date: Date;
  summary: string;
  transcript_file: string;
  action_items: string[];
  decisions: string[];
}

const SummarySchema: Schema = new Schema(
  {
    team: { type: String, required: true },
    date: { type: Date, required: true },
    summary: { type: String, required: true },
    transcript_file: { type: String },
    action_items: { type: [String], default: [] },
    decisions: { type: [String], default: [] },
  },
  { timestamps: true }
);

// Prevent model overwrite on hot reloads
export default models.Summary || mongoose.model<ISummary>("Summary", SummarySchema);
