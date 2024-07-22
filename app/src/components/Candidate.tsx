import React from 'react';
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { ChevronRightIcon } from "@/components/icons";
import Link from 'next/link';

interface CandidateProps {
  name: string;
  stage: string;
  relevancyScore: number;
  id: string;
}

const Candidate: React.FC<CandidateProps> = ({ id, name, stage, relevancyScore }) => {
  return (
    <div className="grid gap-4 border rounded-lg p-4">
      <div className="flex items-center gap-4">
        <Avatar className="w-12 h-12">
          <AvatarImage src="/placeholder-user.jpg" />
          <AvatarFallback>{name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
        </Avatar>
        <div className="grid gap-1">
          <div className="font-semibold">{name}</div>
          <div className="font-semibold">Stage: {stage}</div>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <div className="text-sm font-medium">Relevancy Score</div>
          <div className="flex items-center gap-1">
            <div className="w-16 h-4 rounded-full bg-muted">
              <div className="h-full rounded-full bg-primary" style={{ width: `${relevancyScore}%` }} />
            </div>
            <div className="text-sm font-medium">{relevancyScore}%</div>
          </div>
        </div>
      </div>
      <Link href={`/candidate/${id}`} className="flex items-center gap-2 font-medium [&[data-state=open]>svg]:rotate-90">
        Career Summary
        <ChevronRightIcon className="w-4 h-4 transition-all" />
      </Link>
    </div>
  );
};

export default Candidate;