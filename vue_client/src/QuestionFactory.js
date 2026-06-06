export const QuestionFactory = {
    create(config, context) {
        if (config.type === 'multiplication') {
            return this.buildMultiplication(config, context);
        }
        if (config.type === 'addition') {
            return this.buildAddition(config, context);
        }
        if (config.type === 'subtraction') {
            return this.buildSubtraction(config, context);
        }
        if (config.type === 'division') {
            return this.buildDivision(config, context);
        }
        throw new Error("Unknown generator type: " + config.type);
    },

    _pickBaseNumbers(context) {
        let n1 = 0, n2 = 0;
        if (context.gameMode === 'total') {
            const maxIndex = context.gridColumns.length;
            n1 = Math.floor(Math.random() * maxIndex);
            n2 = Math.floor(Math.random() * maxIndex);
        } else if (context.gameMode === 'weak' && context.weakSpots.length > 0) {
            const spot = context.weakSpots[Math.floor(Math.random() * context.weakSpots.length)];
            n1 = spot[0];
            n2 = spot[1];
        } else {
            const r = Math.random();
            if (r <= 0.50 && context.untestedPairs.length > 0) {
                const spot = context.untestedPairs[Math.floor(Math.random() * context.untestedPairs.length)];
                n1 = spot[0];
                n2 = spot[1];
            } else if (r > 0.75 && context.weakSpots.length > 0) {
                const spot = context.weakSpots[Math.floor(Math.random() * context.weakSpots.length)];
                n1 = spot[0];
                n2 = spot[1];
            } else {
                const poolIndex1 = Math.floor(Math.random() * context.unlockedNumbers.length);
                const poolIndex2 = Math.floor(Math.random() * context.unlockedNumbers.length);
                n1 = context.unlockedNumbers[poolIndex1];
                n2 = context.unlockedNumbers[poolIndex2];
            }
        }
        return [n1, n2];
    },

    buildMultiplication(config, context) {
        let [n1, n2] = this._pickBaseNumbers(context);

        if (config.allowNegatives) {
            if (Math.random() > 0.5 && n1 !== 0) n1 *= -1;
            if (Math.random() > 0.5 && n2 !== 0) n2 *= -1;
        }

        const displayOrder = Math.random() > 0.5 ? [n1, n2] : [n2, n1];
        const n2Str = displayOrder[1] < 0 ? `(${displayOrder[1]})` : `${displayOrder[1]}`;
        
        const min = Math.min(n1, n2);
        const max = Math.max(n1, n2);

        return {
            num1: displayOrder[0],
            num2: displayOrder[1],
            displayString: `${displayOrder[0]} × ${n2Str}`,
            correctAnswer: n1 * n2,
            trackingKey: `${min}x${max}`
        };
    },

    buildAddition(config, context) {
        let [n1, n2] = this._pickBaseNumbers(context);

        if (config.allowNegatives) {
            if (Math.random() > 0.5 && n1 !== 0) n1 *= -1;
            if (Math.random() > 0.5 && n2 !== 0) n2 *= -1;
        }

        const displayOrder = Math.random() > 0.5 ? [n1, n2] : [n2, n1];
        const n2Str = displayOrder[1] < 0 ? `(${displayOrder[1]})` : `${displayOrder[1]}`;
        
        const min = Math.min(n1, n2);
        const max = Math.max(n1, n2);

        return {
            num1: displayOrder[0],
            num2: displayOrder[1],
            displayString: `${displayOrder[0]} + ${n2Str}`,
            correctAnswer: n1 + n2,
            trackingKey: `add_${min}+${max}`
        };
    },

    buildSubtraction(config, context) {
        let [n1, n2] = this._pickBaseNumbers(context);

        // For standard subtraction, we usually want the bigger number first so the answer is positive
        let top = Math.max(n1, n2);
        let bottom = Math.min(n1, n2);

        // Unless they have "allow negatives" checked!
        if (config.allowNegatives && Math.random() > 0.5) {
            top = Math.min(n1, n2);
            bottom = Math.max(n1, n2);
        }

        const bottomStr = bottom < 0 ? `(${bottom})` : `${bottom}`;
        const max = Math.max(top, bottom);
        const min = Math.min(top, bottom);

        // The tracking key maps it exactly to the Mastery Grid (e.g. "sub_12-7")
        return {
            num1: top,
            num2: bottom,
            displayString: `${top} - ${bottomStr}`,
            correctAnswer: top - bottom,
            trackingKey: `sub_${max}-${min}`
        };
    },

    buildDivision(config, context) {
        let [n1, n2] = this._pickBaseNumbers(context);

        // Prevent Divide by Zero by bumping the divisor to 1
        if (n2 === 0) {
            if (n1 !== 0) { n2 = n1; n1 = 0; } 
            else { n2 = 1; }
        }

        let product = n1 * n2;
        let divisor = n2;
        let quotient = n1;

        if (config.allowNegatives) {
            if (Math.random() > 0.5 && product !== 0) product *= -1;
            if (Math.random() > 0.5 && divisor !== 0) divisor *= -1;
            quotient = product / divisor;
        }

        const divStr = divisor < 0 ? `(${divisor})` : `${divisor}`;
        const min = Math.min(n1, n2);
        const max = Math.max(n1, n2);

        // Tracking key isolates it in the DB while mapping perfectly to the 12x12 grid
        return {
            num1: n1,
            num2: n2,
            displayString: `${product} ÷ ${divStr}`,
            correctAnswer: quotient,
            trackingKey: `div_${min}/${max}`
        };
    }
};