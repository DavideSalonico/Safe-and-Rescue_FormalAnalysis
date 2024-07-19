/*
 * Return an alternative position wrt to next. This function is used when the next cell to go is occupied
 */
pos_t getAlternativeNext(pos_t next){
    pos_t alt1 = OUT_OF_MAP;
    pos_t neighbors[3][3];
    int i, j;
    for(i = 0; i < 3; i++){
        for(j = 0; j < 3; j++){
            if (pos.r + i - 1>= 0 && pos.r + i - 1< GRID_HEIGHT && pos.c + j - 1>= 0 && pos.c + j - 1< GRID_LENGTH){
                neighbors[i][j].r = pos.r + i - 1; 
                neighbors[i][j].c = pos.c + j - 1; 
            }
                
            else neighbors[i][j] = OUT_OF_MAP;
        }
    }

    for(i = 0; i < 3; i++){
        for(j = 0; j < 3; j++){
            if(neighbors[i][j] != OUT_OF_MAP && isCellFree(neighbors[i][j]) && dist(target_fire, neighbors[i][j]) <= (1 + dist(target_fire, next))){
                alt1.r = neighbors[i][j].r;
                alt1.c = neighbors[i][j].c;
            }
        }
    }

    return alt1;
}