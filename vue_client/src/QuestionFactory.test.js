import { describe, it, expect } from 'vitest'
import { QuestionFactory } from './QuestionFactory.js'

describe('QuestionFactory', () => {
    it('generates a valid multiplication question', () => {
        const context = {
            gameMode: 'campaign',
            unlockedNumbers: [0, 1, 2],
            gridColumns: [0, 1, 2, 3, 4, 5],
            untestedPairs: [],
            weakSpots: []
        };
        const config = { type: 'multiplication', allowNegatives: false };

        const question = QuestionFactory.create(config, context);

        expect(question).toHaveProperty('num1');
        expect(question).toHaveProperty('num2');
        expect(question.correctAnswer).toBe(question.num1 * question.num2);
        expect(question.displayString).toContain('×');
    });

    it('generates a valid addition question', () => {
        const context = {
            gameMode: 'total',
            gridColumns: [0, 1, 2, 3],
            unlockedNumbers: [0, 1, 2],
            untestedPairs: [],
            weakSpots: []
        };
        const config = { type: 'addition', allowNegatives: false };

        const question = QuestionFactory.create(config, context);

        expect(question.correctAnswer).toBe(question.num1 + question.num2);
        expect(question.displayString).toContain('+');
    });

    it('forces negative numbers when allowed', () => {
        const context = {
            gameMode: 'weak',
            weakSpots: [[-5, 5]], // Force it to pick this exact spot
            unlockedNumbers: [],
            gridColumns: [],
            untestedPairs: []
        };
        const config = { type: 'multiplication', allowNegatives: true };

        const question = QuestionFactory.create(config, context);
        
        // Since we forced the weak spot to be -5 and 5, the answer must be -25
        expect(question.correctAnswer).toBe(-25);
    });
})