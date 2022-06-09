import { cron, jetroutine } from 'jetpack-io';

cron(
  'exampleCron',
  '30 * * * *',
  () => {
    console.log('executing exampleCron!');
  },
);

export const exampleJetroutine = jetroutine(
  'exampleJetroutine',
  () => {
    console.log('hello from example jetroutine!');
  }
)
