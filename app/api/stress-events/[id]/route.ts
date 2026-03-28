import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { stressSchema } from '@/lib/validation';

export async function PUT(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const payload = stressSchema.parse(await req.json());
    const { id } = await params;
    const updated = await prisma.stressEvent.update({
      where: { id },
      data: {
        title: payload.title,
        description: payload.description || null,
        stressIncrease: payload.stressIncrease,
        currentIntensity: payload.currentIntensity,
        triggerCategory: payload.triggerCategory,
        copingUsed: payload.copingUsed || null,
        enteredAutopilot: payload.enteredAutopilot
      }
    });
    return NextResponse.json(updated);
  } catch {
    return NextResponse.json({ error: 'Unable to update stress event.' }, { status: 400 });
  }
}

export async function DELETE(_: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await prisma.stressEvent.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ error: 'Unable to delete stress event.' }, { status: 400 });
  }
}
