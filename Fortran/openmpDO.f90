PROGRAM testopenmp
    INTEGER ::i,j,k(100000)
    !$OMP parallel
    !$OMP DO
        DO i=1,99999
            DO j=1,100000
                k(i)=i+j
            END DO
        END DO
        !$OMP END DO
    !$OMP END parallel
END PROGRAM
