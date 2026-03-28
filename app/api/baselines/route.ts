import { NextResponse } from 'next/server';
import { DEFAULT_USER_ID } from '@/lib/constants';
import { prisma } from '@/lib/db';
import { ensureDefaultUser } from '@/lib/data';
import { baselineSchema } from '@/lib/validation';

export async function GET() {
  await ensureDefaultUser();
  const entries = await prisma.baselineEntry.findMany({ where: { userId: DEFAULT_USER_ID }, orderBy: { date: 'desc' } });
  return NextResponse.json(entries);
}

export async function POST(req: Request) {
  try {
    const payload = baselineSchema.parse(await req.json());
    await ensureDefaultUser();

    const date = new Date(payload.date);
    const normalizedDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());

    const result = await prisma.baselineEntry.upsert({
      where: { userId_date: { userId: DEFAULT_USER_ID, date: normalizedDate } },
      update: {
        baselineIntensity: payload.baselineIntensity,
        notes: payload.notes || null
      },
      create: {
        userId: DEFAULT_USER_ID,
        date: normalizedDate,
        baselineIntensity: payload.baselineIntensity,
        notes: payload.notes || null
      }
    });

    return NextResponse.json(result, { status: 201 });
  } catch {
    return NextResponse.json({ error: 'Invalid baseline entry.' }, { status: 400 });
  }
}
