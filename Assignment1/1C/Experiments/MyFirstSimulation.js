// Run with: node MyFirstSimulation.js

let CPM = require("./artistoo_minimal/build/artistoo-cjs.js")

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
		torus : [true,true],// Border. True = wrapped. False=borders.
		// seed : 4,							// Seed for random number generation.
		T : 20,								// CPM temperature

		// Constraint parameters.
		// Mostly these have the format of an array in which each element specifies the
		// parameter value for one of the cellkinds on the grid.
		// First value is always cellkind 0 (the background) and is often not used.

		// Adhesion parameters: [background, obstacle, moving cell]
		J: [[0,20,20], [20,0,1000], [20,1000,0]],

		// VolumeConstraint parameters
		LAMBDA_V: [0,50,500],					// Obstacle rigid, moving cell flexible
		V: [0,200,100],							// Same size for both

		// PerimeterConstraint parameters
		LAMBDA_P: [0,2,200],
		P : [0,180,50],

		// ActivityConstraint parameters
		LAMBDA_ACT : [0,200,0],				// Obstacle has NO activity
		MAX_ACT : [0,20,0],					// Obstacle cannot move
		ACT_MEAN : "geometric"

	},

	// Simulation setup and configuration
	simsettings : {

		// Cells on the grid - set to [0,0] since we manually place obstacles and seed cells below
		NRCELLS : [40, 0],

		NUM_OBSTACLES : 0, // Number of obstacles. Keep square (3x3, 4x4, 5x5....). 
		OBSTACLE_RADIUS : 6, // Just places pixels in that radius. Then V and P determine final shape and size of obstacles.
		OBSTACLE_PADDING : 10, // Padding from borders. 25 is golden, but can always adjust if changing NUM_OBSTACLES or field size.

		// Runtime etc
		BURNIN : 0,
		RUNTIME : 900,

		FRAMERATE : 1,
		// Visualization
		CANVASCOLOR : "eaecef",
		CELLCOLOR : ["000000", "888888"],  // Blue obstacle, black moving cell
		ACTCOLOR : [true, false],
		SHOWBORDERS : [false, false],
		zoom : 2,

		// Output images
		SAVEIMG : true,
		IMGFRAMERATE : 1,
		SAVEPATH : "img",
		EXPNAME : "simulation",

		// Output stats etc
		STATSOUT : { browser: false, node: true },
		LOGRATE : 10

	}
}
/*	---------------------------------- */

// Initialize simulation
let sim = new CPM.Simulation( config )

function buildObstacles(){
	const numObstacles = config.simsettings.NUM_OBSTACLES
	
	if( numObstacles === 0 ){
		return
	}
	
	const gridSize = Math.sqrt(numObstacles)
	const radius = config.simsettings.OBSTACLE_RADIUS
	const padding = config.simsettings.OBSTACLE_PADDING
	
	const xSpacing = Math.floor((config.field_size[0] - 2 * padding) / (gridSize - 1))
	const ySpacing = Math.floor((config.field_size[1] - 2 * padding) / (gridSize - 1))
	
	// Create obstacle cells (cellkind 2)
	for( let i = 0; i < gridSize; i++ ){
		for( let j = 0; j < gridSize; j++ ){
			const centerX = padding + xSpacing * i
			const centerY = padding + ySpacing * j
			
			// Create a new obstacle cell
			const obstacleID = sim.C.makeNewCellID( 2 )
			
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

// Seed moving cells
for(let i = 0; i < config.simsettings.MANUAL_CELL_COUNT; i++){
	sim.gm.seedCell(2)
}

// Run simulation
sim.run()
