// Run with: node Final_final4.js [--cells N] [--obstacles N]
// Examples:
//   node Final_final4.js
//   node Final_final4.js --cells 120 --obstacles 16
//   node Final_final4.js --cells 50 --obstacles 25

let CPM = require("./Experiments/artistoo_minimal/build/artistoo-cjs.js")

// Parse command line arguments
let args = process.argv.slice(2)
let cliCells = null
let cliObstacles = null

for(let i = 0; i < args.length; i++){
	if(args[i] === "--cells" && i + 1 < args.length){
		cliCells = parseInt(args[i + 1])
		i++
	} else if(args[i] === "--obstacles" && i + 1 < args.length){
		cliObstacles = parseInt(args[i + 1])
		i++
	}
}

/*	----------------------------------
	CONFIGURATION SETTINGS
	----------------------------------
*/
let config = {
	// Grid settings
	ndim : 2,
	field_size : [200,200],

	// CPM parameters and configuration
	conf : {
		// Basic CPM parameters
		torus : [true,true],
		T : 20,

		// Adhesion parameters: [background, moving cell, obstacle]
		J: [[0,20,20], [20,0,1000], [20,1000,0]],
		
		// VolumeConstraint parameters
		LAMBDA_V: [0,50,500],      // Obstacles are rigid (high lambda)
		V: [0,200,100],            // Obstacle volume ~130 pixels (radius 6.5)
		
		// PerimeterConstraint parameters
		LAMBDA_P: [0,2,200],       // Obstacles maintain shape (high lambda)
		P : [0,180,50],
		
		// ActivityConstraint parameters
		LAMBDA_ACT : [0,200,0],    // Obstacles don't move (0 activity)
		MAX_ACT : [0,60,0],        // Obstacles don't move
		ACT_MEAN : "geometric"
	},

	// Simulation setup and configuration
	simsettings : {
		NRCELLS : [0, 0], // Keep 0 here, cells are seeded manually below
		NUM_OBSTACLES : cliObstacles !== null ? cliObstacles : 0,
		OBSTACLE_RADIUS : 6,
		OBSTACLE_PADDING : 10,
		MANUAL_CELL_COUNT : cliCells !== null ? cliCells : 60,

		BURNIN : 100,
		RUNTIME : 2400,

		CANVASCOLOR : "eaecef",
		CELLCOLOR : ["000000", "888888"],  // Moving cells black, obstacles gray
		ACTCOLOR : [true, false],          // Show activity for moving cells only
		SHOWBORDERS : [false, false],
		zoom : 2,

		SAVEIMG : true,
		IMGFRAMERATE : 1,
		SAVEPATH : "img",
		EXPNAME : "simulation",

		STATSOUT : { browser: false, node: true },
		LOGRATE : 10
	}
}
/*	---------------------------------- */

// Initialize simulation
let sim = new CPM.Simulation( config )

function buildObstacles(){
	let numObstacles = config.simsettings.NUM_OBSTACLES

	if( numObstacles === 0 ){
		return
	}

	let gridSize = Math.sqrt(numObstacles)
	let radius = config.simsettings.OBSTACLE_RADIUS
	let padding = config.simsettings.OBSTACLE_PADDING

	let xSpacing = Math.floor((sim.C.extents[0] - 2 * padding) / (gridSize - 1))
	let ySpacing = Math.floor((sim.C.extents[1] - 2 * padding) / (gridSize - 1))

	// Create obstacle cells (cellkind 2)
	for( let i = 0; i < gridSize; i++ ){
		for( let j = 0; j < gridSize; j++ ){
			let centerX = padding + xSpacing * i
			let centerY = padding + ySpacing * j

			// Create a new obstacle cell
			let obstacleID = sim.C.makeNewCellID( 2 )

			// Place pixels for this obstacle
			for( let xx = centerX - radius; xx <= centerX + radius; xx++ ){
				for( let yy = centerY - radius; yy <= centerY + radius; yy++){
					let dx = Math.abs( xx - centerX )
					let dy = Math.abs( yy - centerY )
					if( Math.sqrt( dx*dx + dy*dy ) < radius ){
						sim.C.setpix( [xx, yy], obstacleID )
					}
				}
			}
		}
	}
}

// Place obstacles first
buildObstacles()

// Seed moving cells (cellkind 1)
for( let i = 0; i < config.simsettings.MANUAL_CELL_COUNT; i++ ){
	sim.gm.seedCell( 1 )
}

// Run simulation
sim.run()
