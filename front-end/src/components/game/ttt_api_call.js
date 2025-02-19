import API from '@/api.js';

export async function getProfile() {
  try {
    const response = await API.get('/api/profile/');
    return { username: response.data.username, id: response.data.id };
  } catch (error) {
    console.error("Error fetching profile:", error);
    return {};
  }
}

export async function getAI() {
  try {
    const response = await API.get('/api/profile/AI');
    return { username: response.data.username, id: response.data.id };
  } catch (error) {
    console.error("Error fetching AI profile:", error);
    return {};
  }
}

export async function postGameResult(p1, p2, winner, p1Turns, p2Turns) {
  try {
    await API.post('/api/games/ttt/', {
      player1: p1,
      player2: p2,
      winner: winner,
      loser: winner === p1 ? p2 : p1,
      player1_turn: p1Turns,
      player2_turn: p2Turns,
    });
  } catch (error) {
    console.error("Error posting game result:", error);
  }
}

export async function patchGameStats(result, turns) {
  let win_loss;
  if (result === 1) {
    win_loss = 'stat_ttt_wins_tot';
  } else {
    win_loss = 'stat_ttt_loss_tot';
  }
  let tot_turn;

  switch (turns) {
    case 'win_5':
      tot_turn = 'stat_ttt_wins_tot_min5';
      break;
    case 'loss_5':
      tot_turn = 'stat_ttt_loss_tot_min5';
      break;
    case 'win_10':
      tot_turn = 'stat_ttt_wins_tot_min10';
      break;
    case 'loss_10':
      tot_turn = 'stat_ttt_loss_tot_min10';
      break;
    case 'win_15':
      tot_turn = 'stat_ttt_wins_tot_max10';
      break;
    case 'loss_15':
      tot_turn = 'stat_ttt_loss_tot_max10';
      break;
  }

  try {
    console.log(win_loss, ": 1", tot_turn, ": 1");
    await API.patch('/api/stats_ttt/', {
      [win_loss]: 1,
      [tot_turn]: 1,
    });
  } catch (error) {
    console.error("Error patching game stats:", error);
  }
}