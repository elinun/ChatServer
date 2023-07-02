function encrypt(text, password) {
	var plainBytes = toBytes(text);
	var keyBytes = toBytes(password);
	var key = arrToMatrix(keyBytes);
	while (plainBytes.length % key.length != 0) {
		plainBytes[plainBytes.length] = 0;
	}
	
	cipherarr = [];
	for (var i = 0; i < plainBytes.length; i+=key.length) {
		var vectorI = [];
		for (var j = 0; j < key.length; j++) {
			vectorI[j] = plainBytes[(i*key.length)+j];
		}
		cipherarr[i] = multiplyMatrixByVector(key, vectorI);
	}
	cipherarr = cipherarr.flat();
	return cipherarr;
}

function decrypt(ciphertext, password) {
	var bytes = toBytes(ciphertext);
	var keyBytes = toBytes(password);
	var key = arrToMatrix(keyBytes);
	key = invertMatrix(key);
	while (bytes.length % key.length != 0) {
		bytes[bytes.length] = 0;
	}
	
	plainarr = [];
	for (var i = 0; i < bytes.length; i+=key.length) {
		var vectorI = [];
		for (var j = 0; j < key.length; j++) {
			vectorI[j] = bytes[(i*key.length)+j];
		}
		plainarr[i] = multiplyMatrixByVector(key, vectorI);
	}
	plainarr = plainarr.flat();
	return plainarr;
}


function arrToMatrix(arr) {
	var matrix = [];
	var dim = Math.sqrt(arr.length);
	for (var i = 0; i < dim; i++) {
		var col = [];
		for (var j = 0; j < dim; j++) {
			col[j] = arr[(i*dim)+j];
		}
		matrix[i] = col;
	}
}

function toBytes(inString) {
	var outArr = [];
	for(var i = 0; i < inString.length; i++) {
		outArr[i] = inString.charAt(i);
	}
	return outArr;
}

function toStr(inBytes) {
	var retStr = "";
	for (var i = 0; i < inBytes.length; i++) {
		retStr += String.fromCharCode(inBytes[i]);
	}
}

//matrix here is defined as an array of COLUMN vectors(arrays)
function multiplyMatrixByVector(matrix, vector) {
	var product = [];
	for (var v = 0; v < vector.length; v++) {
		var sum = 0;
		for (var c = 0; c < matrix.length; c++) {
			sum += matrix[c][v] * vector[v];
		}
		product[v] = sum;
	}
	return product;
}

function invertMatrix(matrix) {
	//https://www.geeksforgeeks.org/adjoint-inverse-matrix/
    //if (rows != cols)
     //   throw new exception("Can not calculate inverse of non-square matrix");

    //Augment Identity matrix to the right of matrix
	var rows = matrix[0].length;
    var augmentedMatrix = matrix.concat([[1, 0, 0], [0, 1, 0], [0, 0, 1]]);




    //RREF
    //https://en.wikipedia.org/wiki/Gaussian_elimination#Pseudocode
    //https://stackoverflow.com/questions/31756413/solving-a-simple-matrix-in-row-reduced-form-in-c
    var lead = 0;
    var A = augmentedMatrix;

    while (lead < rows) {

        for (int r = 0; r < rows; r++) { // for each row ...
            /* calculate divisor and multiplier */
            var d = A[lead][lead];
            var m = A[lead][r] / A[lead][lead];

            for (int c = 0; c < augmentedMatrix.size(); c++) { // for each column ...
                if (r == lead)
                    A[c][r] /= d;               // make pivot = 1
                else
                    A[c][r] -= A[c][lead] * m;  // make other = 0
            }
        }

        lead++;
        //test_print(A);
    }

    //Grab the relevant columns
    return A.slice(matrix.length, A.length);
}