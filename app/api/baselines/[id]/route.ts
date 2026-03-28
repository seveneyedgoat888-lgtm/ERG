import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { baselineSchema } from '@/lib/validation';

export async function PUT(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const payload = baselineSchema.parse(await req.json());
    const { id } = await params;
    const date = new Date(payload.date);
    const normalizedDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());

    const updated = await prisma.baselineEntry.update({
      where: { id },
      data: {
        date: normalizedDate,
        baselineIntensity: payload.baselineIntensity,
        notes: payload.notes || null
      }
    });

    return NextResponse.json(updated);
  } catch {
    return NextResponse.json({ error: 'Unable to update baseline entry.' }, { status: 400 });
  }
}

export async function DELETE(_: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await prisma.baselineEntry.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ error: 'Unable to delete baseline entry.' }, { status: 400 });
  }
}
