import { NextResponse } from "next/server";
import dbConnect from "@/app/lib/mongodb";
import Summary from "@/app/models/summary";

export async function GET(
  req: Request,
  { params }: { params: { id: string } }
) {
  try {
    await dbConnect();

    // Query meetings by team field matching the incoming id
    const meetings = await Summary.find({ team: params.id }).lean();

    if (meetings.length === 0) {
      return NextResponse.json(
        { error: "No meetings found for this team" },
        { status: 404 }
      );
    }

    return NextResponse.json(meetings, { status: 200 });
  } catch (err) {
    console.error(err);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
