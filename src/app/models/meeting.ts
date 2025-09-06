// models/Meeting.ts
import mongoose from "mongoose";

const MeetingSchema = new mongoose.Schema({
  summary: String,
  action_items: [
    {
      task: String,
      status: String,
      owners: [String],
      due_dates: [String],
    }
  ],
  decisions: [
    { decision: String }
  ],
  team: String, // or whatever identifier you use
});

export default mongoose.models.Meeting || mongoose.model("Meeting", MeetingSchema);
