<template>
    <div class="game-stats-card">
      <h2>{{ gameType }}</h2>
      <div class="stats-list">
        <div v-if="gameType !== 'Tic Tac Toe'" class="stat-item">
          <strong>{{ $t("current-rank") }}</strong> {{ stats.currentRank || ' N/A' }}
        </div>
        <div class="stat-item">
          <strong>{{ $t("total-game") }}</strong> {{ stats.totalMatches || " N/A" }}
        </div>
        <!-- <div class="stat-item">
          <strong>{{ $t("tournament-won") }}</strong> {{ stats.tournamentWins || " N/A" }}
        </div> -->
      </div>
      
      <div class="charts-container">
        <div class="chart" v-if="gameType !== 'Tic Tac Toe'" >
          <h3>{{ $t("rank-progress") }}</h3>
          <Line :data="rankProgressionData" :options="chartOptions" />
        </div>
        <div class="chart">
          <h3>{{ $t("win/loss-ratio") }}</h3>
          <Doughnut :data="winLossData" :options="chartOptions" />
        </div>
        <div class="chart" v-if="gameType !== 'Tic Tac Toe'">
          <h3>{{ $t("point-exchange") }}</h3>
          <Bar :data="pointExchangeData" :options="chartOptions" />
        </div>
        <div class="chart" v-if="gameType === 'Tic Tac Toe'">
          <h3>{{ $t("win-on-x-moves") }}</h3>
          <Bar :data="moveExchangeData" :options="chartOptions" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Line, Doughnut, Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, ArcElement, BarElement } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, ArcElement, BarElement)
  
  export default {
    name: 'GameStatsCard',
    components: {
      Line,
      Doughnut,
      Bar
    },
    props: {
      gameType: {
        type: String,
        required: true
      },
      stats: {
        type: Object,
        required: true
      }
    },
    computed: {
      rankProgressionData() {
        if (!this.stats || !Array.isArray(this.stats.rankProgression)) {
          // console.warn('Missing or invalid rankProgression data for', this.gameType, this.stats);
          return { labels: [], datasets: [] };
        }
        console.log("stats", this.stats);
        const progression = this.stats.rankProgression;
        //console.log("progres :", progression);
        //console.debug("Rank Progression for", this.gameType, progression);
        return {
          labels: progression.map((_, index) => `Match ${index}`),
          datasets: [{
            label: 'rank-points',
            data: progression,
            borderColor: '#36A2EB',
            tension: 0.1,
            fill: false
          }]
        }
      },
      winLossData() {
        const wins = this.stats.wins !== undefined ? this.stats.wins : 0;
        const losses = this.stats.losses !== undefined ? this.stats.losses : 0;
        if (wins === 0 && losses === 0) {
          // console.warn('No win/loss data for', this.gameType, this.stats);
        }
        // console.debug("Win/Loss for", this.gameType, { wins, losses });
        return {
          labels: ['Wins', 'Losses'],
          datasets: [{
            data: [wins, losses],
            backgroundColor: ['#36A2EB', '#FF6384']
          }]
        }
      },
      pointExchangeData() {
        const pointsWonUnder5 = this.stats.pointsWonUnder5Exchanges || 0;
        const pointsWonUnder10 = this.stats.pointsWonUnder10Exchanges || 0;
        const pointsWonOver10 = this.stats.pointsWonOver10Exchanges || 0;
        const pointsLostUnder5 = this.stats.pointsLostUnder5Exchanges || 0;
        const pointsLostUnder10 = this.stats.pointsLostUnder10Exchanges || 0;
        const pointsLostOver10 = this.stats.pointsLostOver10Exchanges || 0;
        
        // console.debug("Point Exchange for", this.gameType, {
        //   pointsWonUnder5, pointsWonUnder10, pointsWonOver10,
        //   pointsLostUnder5, pointsLostUnder10, pointsLostOver10
        // });
        
        return {
          labels: ['< 5 exchanges', '5-10 exchanges', '> 10 exchanges'],
          datasets: [
            {
              label: 'Points Won',
              data: [pointsWonUnder5, pointsWonUnder10, pointsWonOver10],
              backgroundColor: '#36A2EB'
            },
            {
              label: 'Points Lost',
              data: [pointsLostUnder5, pointsLostUnder10, pointsLostOver10],
              backgroundColor: '#FF6384'
            }
          ]
        }
      },
      moveExchangeData() {
        const pointsWonUnder5 = this.stats.pointsWonUnder5Moves || 0;
        const pointsWonUnder10 = this.stats.pointsWonUnder10Moves || 0;
        const pointsWonOver10 = this.stats.pointsWonOver10Moves || 0;
        const pointsLostUnder5 = this.stats.pointsLostUnder5Moves || 0;
        const pointsLostUnder10 = this.stats.pointsLostUnder10Moves || 0;
        const pointsLostOver10 = this.stats.pointsLostOver10Moves || 0;
        
        return {
          labels: ['< 5 moves', '5-10 moves', '> 10 moves'],
          datasets: [
            {
              label: 'Moves to Won',
              data: [pointsWonUnder5, pointsWonUnder10, pointsWonOver10],
              backgroundColor: '#36A2EB'
            },
            {
              label: 'Moves to Lost',
              data: [pointsLostUnder5, pointsLostUnder10, pointsLostOver10],
              backgroundColor: '#FF6384'
            }
          ]
        }
      },
      chartOptions() {
        return {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              ticks: { color: '#fff' },
              grid: { color: 'rgba(255,255,255,0.1)' }
            },
            y: {
              ticks: { color: '#fff' },
              grid: { color: 'rgba(255,255,255,0.1)' }
            }
          },
          plugins: {
            legend: {
              labels: { color: '#fff' }
            },
            title: { display: false }
          }
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .game-stats-card {
    background: var(--text-box-color);
    border-radius: 8px;
    padding-bottom: 50px;
    padding-top: 10px;
    margin-bottom: 20px;
}
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .stat-item {
    background-color: var(--background-dark);
    padding: 3px;
    border-radius: 4px;
    display: flex;
    margin-left: 30px;
  }
  
  .charts-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .chart {
    background-color: var(--background-dark);
    padding: 15px;
    border-radius: 4px;
    position: relative;
    height: 300px;
    margin-bottom: 50px;
  }
  </style>
  