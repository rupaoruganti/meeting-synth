import { NextResponse } from "next/server";
import dbConnect from "@/app/lib/mongodb";
import User from "@/app/models/user";

export async function POST(req: Request) {
  try {
    await dbConnect();

    const body = await req.json();
    const { name, email, phone, password, role, domain, reports_to } = body;

    if (!name || !email || !phone || !password || !role) {
      return NextResponse.json(
        { success: false, error: "Missing fields" },
        { status: 400 }
      );
    }

    // ✅ Map team_id properly - Fixed role matching
    let team_id = "";
    const cleanRole = role.toLowerCase().trim().replace(/\s+/g, "");
    const cleanDomain = domain?.toLowerCase().trim();

    if (cleanRole === "vicepresident") {
      team_id = "vp";
    } else if (cleanRole === "projectlead") { // ✅ Fixed: was "team lead", now "projectlead"
      team_id = `team_${cleanDomain || "general"}`; // ✅ Store as "team_frontend", "team_backend", etc.
    } else if (cleanRole === "teammate") {
      team_id = `team_${cleanDomain || "general"}`; // ✅ Store as "team_frontend", "team_backend", etc.
    }

    const newUser = new User({
      name,
      email,
      phone_number: phone,
      password, // saved directly (no bcrypt)
      role,
      team_id,
      reports_to: reports_to || null,
    });

    await newUser.save();

    return NextResponse.json({ success: true, user: newUser });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}