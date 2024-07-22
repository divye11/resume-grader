import React from 'react';
import { Card, CardContent } from "@/components/ui/card"
import Link from 'next/link';
import {CalendarIcon, LocateIcon} from './icons';


type JobsProps = {
   jobData: Job[] | null
}

const Jobs: React.FC<JobsProps> = ({ jobData }) => {
   if (!jobData || jobData.length === 0) {
      return null;
   }

   return jobData.map((job) => (
      <Link href={`/jobdetail/${job.shortcode}`} key={job.id}>
         <Card className="cursor-pointer">
            <CardContent>
               <div className="flex items-start justify-between pt-6">
                  <div className="space-y-1">
                     <h3 className="text-lg font-semibold">
                        <Link href={`/jobdetail/${job.shortcode}`} className="hover:underline" prefetch={false}>
                           {job.full_title}
                        </Link>
                     </h3>
                     <div className="text-sm text-muted-foreground">#{job.shortcode}</div>
                  </div>
                  <Link
                     href={`/jobdetail/${job.shortcode}`}
                     className="inline-flex items-center gap-1 rounded-md bg-primary px-3 py-1 text-xs font-medium text-primary-foreground transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                     prefetch={false}
                  >
                     Open
                  </Link>
               </div>
               <div className="mt-4 flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                     <LocateIcon className="h-4 w-4" />
                     {job.location?.location_str}
                  </div>
                  <div className="flex items-center gap-1">
                     <CalendarIcon className="h-4 w-4" />
                     Created: {job.created_at}
                  </div>
                  <div className="flex items-center gap-1">
                     <CalendarIcon className="h-4 w-4" />
                     Updated: {job.created_at}
                  </div>
               </div>
            </CardContent>
         </Card>
      </Link>
   ));
};

export default Jobs;