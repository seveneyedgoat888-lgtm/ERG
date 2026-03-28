import { PrismaClient, TriggerCategory } from '@prisma/client';
import { addDays } from 'date-fns';

const prisma = new PrismaClient();

async function main() {
  const user = await prisma.user.upsert({
    where: { id: 'default-user' },
    update: {},
    create: { id: 'default-user' }
  });

  const baselineStart = addDays(new Date(), -8);
  for (let i = 0; i < 8; i += 1) {
    const date = addDays(baselineStart, i);
    await prisma.baselineEntry.upsert({
      where: {
        userId_date: {
          userId: user.id,
          date: new Date(date.getFullYear(), date.getMonth(), date.getDate())
        }
      },
      update: {},
      create: {
        userId: user.id,
        date: new Date(date.getFullYear(), date.getMonth(), date.getDate()),
        baselineIntensity: 4 + (i % 3),
        notes: i % 2 === 0 ? 'Demo baseline note' : null
      }
    });
  }

  await prisma.stressEvent.createMany({
    data: [
      {
        userId: user.id,
        title: 'Deadline pressure',
        stressIncrease: 3,
        currentIntensity: 7,
        triggerCategory: TriggerCategory.WORK_OR_SCHOOL,
        copingUsed: '5-minute breathing exercise',
        enteredAutopilot: true
      },
      {
        userId: user.id,
        title: 'Unexpected conflict',
        stressIncrease: 4,
        currentIntensity: 8,
        triggerCategory: TriggerCategory.CONFLICT,
        copingUsed: 'Walk and journal',
        enteredAutopilot: true
      },
      {
        userId: user.id,
        title: 'Loud environment',
        stressIncrease: 2,
        currentIntensity: 6,
        triggerCategory: TriggerCategory.OVERSTIMULATION,
        enteredAutopilot: false
      }
    ]
  });
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
