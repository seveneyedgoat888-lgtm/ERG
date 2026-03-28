import { NextResponse } from 'next/server';
import { DEFAULT_USER_ID } from '@/lib/constants';
import { prisma } from '@/lib/db';
import { ensureDefaultUser } from '@/lib/data';
import { stressSchema } from '@/lib/validation';

export async function GET() {
  await ensureDefaultUser();
  const entries = await prisma.stressEvent.findMany({ where: { userId: DEFAULT_USER_ID }, orderBy: { createdAt: 'desc' } });
  return NextResponse.json(entries);
}

export async function POST(req: Request) {
  try {
    const payload = stressSchema.parse(await req.json());
    await ensureDefaultUser();

    const result = await prisma.stressEvent.create({
      data: {
        userId: DEFAULT_USER_ID,
        title: payload.title,
        description: payload.description || null,
        stressIncrease: payload.stressIncrease,
        currentIntensity: payload.currentIntensity,
        triggerCategory: payload.triggerCategory,
        copingUsed: payload.copingUsed || null,
        enteredAutopilot: payload.enteredAutopilot
      }
    });

    return NextResponse.json(result, { status: 201 });
  } catch {
    return NextResponse.json({ error: 'Invalid stress event.' }, { status: 400 });
  }
}
