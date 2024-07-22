import React from 'react';
import { Card, CardContent } from './ui/card';
import { Skeleton } from './ui/skeleton';


const LoadingState: React.FC = () => {
   return (
      <Card>
         <CardContent>
            <div className="flex items-start justify-between pt-6">
               <div className="space-y-1">
                  <Skeleton className="h-5 w-48" />
                  <Skeleton className="h-4 w-24" />
               </div>
               <Skeleton className="h-6 w-16" />
            </div>
            <div className="mt-4 flex items-center gap-4 text-sm text-muted-foreground">
               <Skeleton className="h-4 w-24" />
               <Skeleton className="h-4 w-24" />
               <Skeleton className="h-4 w-24" />
            </div>
         </CardContent>
      </Card>
   );
};

export default LoadingState;