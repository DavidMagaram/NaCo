const args = require('minimist')(process.argv.slice(2));

// Reading inputs from the console
function getInput( name, defaultValue, type = undefined ){
	if( !args.hasOwnProperty(name)) return defaultValue
	if( type === "boolean" ){ return true }
	else if( type === "int" ){
		if( args[name][0] == "m" ){
			return -parseInt(args[name].substring(1) )
		}
		return parseInt( args[name] )
	}
	else if (type === "float" ){ return parseFloat( args[name] ) }
	else { return args[name] }
}

const fieldsize = getInput( "f", 400, "int" )
const Nboids = getInput( "N", 150, "int" )
const inR = getInput( "i", 10, "int" )
const oR = getInput( "o", 25, "int" )
const wc = getInput( "c", 1, "float" )
const ws = getInput( "s", 1, "float" )
const wa = getInput( "a", 1, "float" )
const runTime = getInput( "T", 300, "int" )

let conf = {
	w : fieldsize,
	h : fieldsize,
	N : Nboids,
	zoom : 1,
	innerRadius : inR,
	outerRadius : oR,
	cohesion : wc,
	separation : ws,
	alignment : wa,
	runTime : runTime
}

class Particle {
	constructor( Scene, i ){
		this.S = Scene
		this.speed = 1
		this.id = i
		this.pos = this.S.randomPosition()
		this.dir = this.S.randomDirection()
	}
	addVectors( a, b ){
		const dim = a.length
		let out = []
		for( let d = 0; d < dim; d++ ){
			out.push( a[d] + b[d] )
		}
		return out
	}
	subtractVectors( a, b ){
		const dim = a.length
		let out = []
		for( let d = 0; d < dim; d++ ){
			out.push( a[d] - b[d] )
		}
		return out
	}
	multiplyVector( a, c ){
		return a.map(( x ) => x * c )
	}
	normalizeVector( a ){
		return this.S.normalizeVector(a)
	}

	alignmentVector( neighborRadius ){
		const neighbors = this.S.neighbours( this, neighborRadius )
		if( neighbors.length === 0 ) return this.dir.slice()
		let avg = [0, 0]
		for( let n of neighbors ){
			avg = this.addVectors( avg, n.dir )
		}
		return this.normalizeVector( avg )
	}

	cohesionVector( neighborRadius ){
		const neighbors = this.S.neighbours( this, neighborRadius )
		if( neighbors.length === 0 ) return this.dir.slice()
		let avgPos = [0, 0]
		for( let n of neighbors ){
			const wrappedPos = this.S.wrap( n.pos, this.pos )
			avgPos = this.addVectors( avgPos, wrappedPos )
		}
		avgPos = avgPos.map( x => x / neighbors.length )
		const toCenter = this.subtractVectors( avgPos, this.pos )
		return this.normalizeVector( toCenter )
	}

	separationVector( neighborRadius ){
		const neighbors = this.S.neighbours( this, neighborRadius )
		if( neighbors.length === 0 ) return this.dir.slice()
		let avgPos = [0, 0]
		for( let n of neighbors ){
			const wrappedPos = this.S.wrap( n.pos, this.pos )
			avgPos = this.addVectors( avgPos, wrappedPos )
		}
		avgPos = avgPos.map( x => x / neighbors.length )
		const awayFromCenter = this.subtractVectors( this.pos, avgPos )
		return this.normalizeVector( awayFromCenter )
	}

	updateVector(){
		let align_weight = this.S.conf.alignment
		let cohesion_weight = this.S.conf.cohesion
		let separation_weight = this.S.conf.separation

		const align = this.multiplyVector( this.alignmentVector( this.S.conf.outerRadius ), align_weight )
		const cohesion = this.multiplyVector(this.cohesionVector( this.S.conf.outerRadius ), cohesion_weight )
		const separation = this.multiplyVector( this.separationVector(this.S.conf.innerRadius ), separation_weight )

		let direction = this.dir.slice()
		direction = this.addVectors( direction, align )
		direction = this.addVectors( direction, cohesion )
		direction = this.addVectors( direction, separation )
		this.dir = this.normalizeVector( direction )

		const move = this.multiplyVector( this.dir, this.speed )
		this.pos = this.S.wrap( this.addVectors( this.pos, move ) )
	}
}

class Scene {
	constructor( conf ){
		this.w = conf.w
		this.h = conf.h
		this.conf = conf
		this.swarm = []
		this.makeSwarm()
		this.time = 0
	}

	reset(){
		this.swarm = []
		this.time = 0
		this.makeSwarm()
	}

	wrap( pos, reference = undefined ){
		if( (typeof reference == 'undefined') ){
			if( pos[0] < 0 ) pos[0] += this.w
			if( pos[1] < 0 ) pos[1] += this.h
			if( pos[0] > this.w ) pos[0] -= this.w
			if( pos[1] > this.h ) pos[1] -= this.h
			return pos
		}
		const pos2 = pos.slice()
		let dx =  pos2[0] - reference[0] , dy = pos2[1] - reference[1]
		if( dx > this.w/2 ) pos2[0] -= this.w
		if( dx < -this.w/2 ) pos2[0] += this.w
		if( dy > this.h/2 ) pos2[1] -= this.h
		if( dy < -this.h/2 ) pos2[1] += this.h
		return pos2
	}

	addParticle(){
		const i = this.swarm.length + 1
		this.swarm.push( new Particle( this, i ) )
	}

	makeSwarm(){
		for( let i = 0; i < this.conf.N; i++ ) this.addParticle()
	}

	randomPosition(){
		let x = Math.random() * this.w
		let y = Math.random() * this.h
		return [x,y]
	}

	randomDirection( dim = 2 ){
		let dir = []
		while(dim-- > 0){
			dir.push(this.sampleNorm())
		}
		this.normalizeVector(dir)
		return dir
	}

	normalizeVector( a ){
		if( a[0] == 0 & a[1] == 0 ) return [0,0]
		let norm = 0
		for( let i = 0 ; i < a.length ; i ++ ){
			norm += a[i]*a[i]
		}
		norm = Math.sqrt(norm)
		for( let i = 0 ; i < a.length ; i ++ ){
			a[i] /= norm
		}
		return a
	}

	sampleNorm(mu=0, sigma=1) {
		let u1 = Math.random()
		let u2 = Math.random()
		let z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(Math.PI*2 * u2)
		return z0 * sigma + mu
	}

	dist( pos1, pos2 ){
		let dx = pos1[0] - pos2[0]
		if( dx > this.w/2 ){ dx -= this.w }
		if( dx < (-this.w/2) ){ dx += this.w }
		let dy = pos1[1] - pos2[1]
		if( dy > this.h/2 ){ dy -= this.h }
		if( dy < ( -this.h/2 ) ){ dy += this.h }
		return Math.sqrt( dx * dx + dy * dy )
	}

	neighbours( x, distanceThreshold ){
		let r = []
		for( let p of this.swarm ){
			if( p.id == x.id ) continue
			if( this.dist( p.pos, x.pos ) <= distanceThreshold ){
				r.push( p )
			}
		}
		return r
	}

	computeOrderParameter(){
		let sum = [0,0]
		for( let p of this.swarm ){
			const dir = p.dir
			const mag = Math.sqrt(dir[0]*dir[0] + dir[1]*dir[1])
			sum[0] += dir[0] / mag
			sum[1] += dir[1] / mag
		}
		const magnitude = Math.sqrt(sum[0]*sum[0] + sum[1]*sum[1])
		return magnitude / this.swarm.length
	}

	computeNearestNeighborDistance(){
		let distances = []
		for( let p of this.swarm ){
			let minDist = Infinity
			for( let q of this.swarm ){
				if( p.id == q.id ) continue
				const d = this.dist(p.pos, q.pos)
				if( d < minDist ) minDist = d
			}
			distances.push(minDist)
		}
		let sum = distances.reduce((a,b)=>a+b,0)
		return sum / distances.length
	}

	step(){
		for( let p of this.swarm ){
			p.updateVector()
		}
		this.time++
	}
}

// Run simulation
const S = new Scene( conf )

// Log at timestep 0
const reportTimesteps = [0, 100, 200, 300]

if( reportTimesteps.includes(0) ){
	console.log(`${S.time},${S.computeOrderParameter()},${S.computeNearestNeighborDistance()}`)
}

for( let t = 1; t <= conf.runTime; t++ ){
	S.step()
	if( reportTimesteps.includes(S.time) ){
		console.log(`${S.time},${S.computeOrderParameter()},${S.computeNearestNeighborDistance()}`)
	}
}
