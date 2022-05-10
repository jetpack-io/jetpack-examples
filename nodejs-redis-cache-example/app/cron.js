import { cron } from 'jetpack-io';

cron(
  'exampleCron',
  () => {
    console.log('executing exampleCron!');
  },
  '30 * * * *',
);
